# region - Importaciones de clases y librerias
from os import path, listdir, rename
from paramiko import SSHClient, AutoAddPolicy

from controller.Log import Log
from controller.utils.Helpers import Helpers
from controller.utils.Configurations import Configurations
# endregion - Importaciones de clases y librerias

# region - Inicialización de clases o variables globales
logger = Log()
helper = Helpers()
config = Configurations()
# endregion - Inicialización de clases o variables globales

class ZentriaSFTP:
    """
        ZentriaSFTP
        ========
        La clase se encargará de gestionar la carga de archivos
        a través de la conexión dada al SFTP de Zentria.
    """
    def __init__(self):
        """ Constructor de clase. """     
        self.__pathRIPS = config.getConfigValue("variables", "pathRutaRIPS")
        
        self.__sshSFTP = helper.desEncriptarData(config.getConfigValue("conexionSFTP", "keySFTP"))
        self.__hostSFTP =  helper.desEncriptarData(config.getConfigValue("conexionSFTP", "hostSFTP"))
        self.__portSFTP =  helper.desEncriptarData(config.getConfigValue("conexionSFTP", "portSFTP"))
        self.__userSFTP =  helper.desEncriptarData(config.getConfigValue("conexionSFTP", "userSFTP"))
        self.__passSFTP =  helper.desEncriptarData(config.getConfigValue("conexionSFTP", "passSFTP"))
        self.__conexionSFTP = None  # Valor inicial para validar existecia de Conexión al SFTP
    
    def crearConexionSFTP(self):
        """
        Este metodo creará una instancia de conexión
        del SFTP mediante PySFTP, y la almacenará en
        uno de los attr iniciales de la clase.
        """
        exito = False
        try:
            self.__conexionSFTP = SSHClient()
            self.__conexionSFTP.set_missing_host_key_policy(AutoAddPolicy())
            self.__conexionSFTP.connect(hostname=self.__hostSFTP, port=self.__portSFTP, username=self.__userSFTP, password=self.__passSFTP)
            exito = True
        except Exception as e:
            logger.registrarLogError(f"Ocurrió un error en la creación de conexión al SFTP, error: {e}", "crearConexionSFTP")
        finally:
            return exito
    
    def desconectarConexionSFTP(self):
        """
        Metodo para cierre de conexión del SFTP
        """
        if self.__conexionSFTP is not None:
            self.__conexionSFTP.close()
            logger.registrarComentario("Cierre de conexión", "La conexión SFTP se ha cerrado con éxito.")
        else:
            logger.registrarComentario("Cierre de conexión", "No existe una conexión abierta de SFTP para cerrar.")

    def __listar_archivos_en_ruta(self, ruta, extension):
        return [f for f in listdir(ruta) if f.endswith(extension)]

    def __manejar_nombre_archivo(self, ruta: str, nombreArchivoActual: str):
        rutaCarpetaRIPS = ruta.replace(nombreArchivoActual, "")
        if not nombreArchivoActual.startswith("0"):
            nuevoNombre = f"0{nombreArchivoActual}"
            rename(ruta, path.join(rutaCarpetaRIPS, nuevoNombre))
            return path.join(rutaCarpetaRIPS, nuevoNombre)
        return ruta

    def __subir_archivo_sftp(self, ftp, local_path, remote_path):
        return ftp.put(local_path, remote_path)

    def __subir_archivos_en_carpeta(self, ftp, carpeta_local):
        for archivo in listdir(carpeta_local):
            ruta_archivo_local = path.join(carpeta_local, archivo)
            if path.isfile(ruta_archivo_local):
                self.__subir_archivo_sftp(ftp, ruta_archivo_local, archivo)

    def __obtener_mes_carpeta_sftp(self, ftp, mes: str):
        carpetasFSTP = ftp.listdir()
        mesCargue = ""
        for carpeta in carpetasFSTP:
            if(mes.lower() in carpeta.lower()):
                mesCargue = carpeta
        return mesCargue

    def listarArchivosRIPS(self, eps: str, fecha: str, relacionEnvio: str):
        """
        Interacción de automatización con datos
        de la carpeta de RIPS que se cargará.
        """
        dictRetorno = {}
        try:
            if len(listdir(self.__pathRIPS)) > 0:
                rutaMesRIPS = path.join(self.__pathRIPS, fecha)
                if len(listdir(rutaMesRIPS)) > 0:
                    rutaRelacionEnvioRIPS = path.join(rutaMesRIPS, eps, relacionEnvio)
                    if len(listdir(rutaRelacionEnvioRIPS)) > 0:
                        archivosPDF = self.__listar_archivos_en_ruta(rutaRelacionEnvioRIPS, '.pdf')
                        archivosZIP = self.__listar_archivos_en_ruta(rutaRelacionEnvioRIPS, '.zip')
                        zipRIPS = archivosZIP[0]
                        certificado_RIPS = archivosPDF[0]
                        dictRetorno =  {
                            "rips": path.join(rutaRelacionEnvioRIPS, zipRIPS),
                            "cert": path.join(rutaRelacionEnvioRIPS, certificado_RIPS)
                        }
        except Exception as e:
            logger.registrarLogError(f"No ha sido posible procesar la petición de archivos RIPS, error: {e}", "listarArchivosRIPS")
        finally:
            return dictRetorno

    def subirRipsSFTP(self, rutas: dict, mes: str):
        """
        Metodo para carga de archivos a la carpeta
        de RIPS dentro del SFTP que utiliza la EPS
        """
        exito = False
        try:
            ftp = self.__conexionSFTP.open_sftp()  # Apertura de conexión SFTP
            ftp.chdir(f"uploads/RIPS/")  # Cambios a carpeta de Uploads/Rips
            carpetaCargue = self.__obtener_mes_carpeta_sftp(ftp, mes)
            ftp.chdir(carpetaCargue)  # Cambios a carpeta del mes que se procesa
            rutaActualizadaRIPS = self.__manejar_nombre_archivo(rutas["rips"], rutas["rips"].split("\\")[-1])
            nombreDestinoRIPS = rutaActualizadaRIPS.split("\\")[-1]
            nombreDestinoCert = rutas["cert"].split("\\")[-1]
            
            self.__subir_archivo_sftp(ftp, rutaActualizadaRIPS, nombreDestinoRIPS)
            self.__subir_archivo_sftp(ftp, rutas["cert"], nombreDestinoCert)

            ftp.close()
            exito = True
        except Exception as e:
            print(e)
            logger.registrarLogError(f"Se detecto un error al intentar subir RIPS, error: {e}", "subirRipsSFTP")
        finally:
            return exito

    def subirArchivosSoportesSFTP(self, mes: str, relacionEnvio: str, fecha: str, eps: str):
        """
        Metodo para carga de archivos de soportes
        al SFTP relacionado con el número de relación
        de envío.
        """
        exito = False
        try:
            ftp = self.__conexionSFTP.open_sftp()  # Apertura de conexión SFTP
            ftp.chdir("uploads/IMAGENES")  # Cambios a carpeta de Uploads/Rips
            carpetasMeses = ftp.listdir()  # Lista de carpetas del root IMAGENES
            mesesSoportes = next((carpeta for carpeta in carpetasMeses if mes.lower() in carpeta.lower()), None)

            if len(mesesSoportes) > 0:
                ftp.chdir(mesesSoportes)
                carpetasRelacionesEnvio = ftp.listdir()
                if(relacionEnvio not in carpetasRelacionesEnvio):
                    ftp.mkdir(relacionEnvio)
                ftp.chdir(relacionEnvio)

                rutaMesRIPS = path.join(self.__pathRIPS, fecha)
                if(len(listdir(rutaMesRIPS)) > 0):
                    rutaRelacionEnvioRIPS = path.join(rutaMesRIPS, eps, relacionEnvio)
                    if(len(listdir(rutaRelacionEnvioRIPS)) > 0):
                        carpetas = [nombre for nombre in listdir(rutaRelacionEnvioRIPS) if path.isdir(path.join(rutaRelacionEnvioRIPS, nombre))]
                        if(len(carpetas) > 0):
                            for carpeta in carpetas:
                                cantidadArchivos = listdir(path.join(rutaRelacionEnvioRIPS, carpeta))
                                if(len(cantidadArchivos) > 0):
                                    self.__subir_archivos_en_carpeta(ftp, path.join(rutaRelacionEnvioRIPS, carpeta))
            ftp.close()  # Cierre de la conexión del SFTP
            exito = True
        except Exception as e:
            print(e)
            logger.registrarLogError(f"Se detecto un error al intentar subir los soportes relacionados, error: {e}", "subirArchivosSoportesSFTP")
        finally:
            return exito
