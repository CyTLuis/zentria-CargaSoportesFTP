# region - Importaciones de clases y librerias
from controller.Log import Log
from content.ZentriaSFTP import ZentriaSFTP
from controller.utils.Configurations import Configurations
# endregion - Importaciones de clases y librerias

# region - Inicialización de clases o variables globales
logger = Log()
config = Configurations()
# endregion - Inicialización de clases o variables globales

class Orquestador:
    """
        Orquestador
        ========
        Esta clase se encargará de orquestar la carga
        de soportes del proyecto Zentria a través del
        SFTP para las distintas entidades involucradas.
    """
    def __init__(self):
        """ Constructor de la clase """
        self.fechaRIPS = ""
        self.epsEjecucion = ""
        self.relacionEnvio = ""
        self.__relacionMeses = {
            "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril", "05": "Mayo", "06": "Junio",
            "07": "Julio", "08": "Agosto", "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
        }

    def orquestarCarga(self):
        """
        Orquestación de la carga de soportes.
        """
        try:
            mesEjecucion = self.__relacionMeses[self.fechaRIPS.split("-")[0]]
            cargue = ZentriaSFTP()

            if cargue.crearConexionSFTP():
                archivosRIPS = cargue.listarArchivosRIPS(self.epsEjecucion, self.fechaRIPS, self.relacionEnvio)

                if(len(archivosRIPS)) > 0:
                    cargarRIPS = cargue.subirRipsSFTP(archivosRIPS, mesEjecucion)
                    if cargarRIPS:
                        logger.registrarComentario("Carga exitosa RIPS", "La carga de RIPS se realizó con éxito.")
                        cargarSoportes = cargue.subirArchivosSoportesSFTP(mesEjecucion, self.relacionEnvio, self.fechaRIPS, self.epsEjecucion)
                        if(cargarSoportes):
                            logger.registrarComentario("Carga exitosa SOPORTES", "Los soportes se han cargado con éxito.")
                        else:
                            logger.registrarLogError("Error en carga de SOPORTES", "Ocurrió un error al intentar cargar los soportes.")
                    else:
                        logger.registrarLogError("Error en carga RIPS", "Ocurrió un error al intentar cargar los RIPS.")
                else:
                    logger.registrarComentario("No hay archivos RIPS", "No se encontraron archivos RIPS para cargar.")
                cargue.desconectarConexionSFTP()
            else:
                logger.registrarLogError("Error en conexión SFTP", "No se pudo establecer la conexión SFTP.")
        except Exception as e:
            logger.registrarLogError("Error en orquestación", f"Ocurrió un error en la orquestación de la carga: {e}")
