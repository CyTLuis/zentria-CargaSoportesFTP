# ===========================================================================
# Importaciones de clases y librerias necesarias en este archivo main
# ===========================================================================

# Region -  Importaciones de archivos o librerias
from sys import argv

from controller.Log import Log
from controller.Impresor import Impresor
from controller.Orquestador import Orquestador
# Endregion - Importaciones de archivos o librerias

# ===========================================================================
# VARIABLES GLOBALES - LOCALES - INICIALIZACION DE OBJETOS
# ===========================================================================

# Region - Instancia de clases de archivos importado
logger = Log()
orq = Orquestador()
consola = Impresor()
# Endregion - Instancia de clases de archivos importado

# Region - Body Metodo Principal
def main(fecha: str = "03-2024", eps: str = "NEPS", relacionEnvio: str = "123456"):
    try: 
        consola.imprimirInicio("Carga Soportes SFTP")
        logger.registroInicioProcesos()
        logger.registrarLogProceso("Inicio de ejecución del proceso")
        
        # Region - Cuerpo de la automatización
        orq.fechaRIPS = fecha
        orq.epsEjecucion = eps
        orq.relacionEnvio = relacionEnvio
        orq.orquestarCarga()
        # Endregion - Cuerpo de la automatización
        
        consola.imprimirFinal()
        logger.registroFinalProcesos()
    except Exception as e:
        logger.registrarLogEror(f"Except del main: {e}", "Ejecución de Main")
        consola.imprimirError(f"Ocurrió un error en la ejecución: {e}")
# Endregion

# Metodo para ejecución del Script, invocando la función main()    
if __name__ == '__main__':
    # Obtención de parametros por argumentos.
    if(len(argv) > 1):
        fecha = argv[1]
        eps= argv[2]
        relacionEnvio= argv[3]
        main(fecha, eps, relacionEnvio)
    else:
        main()
