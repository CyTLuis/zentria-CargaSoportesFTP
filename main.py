# ===========================================================================
# Importaciones de clases y librerias necesarias en este archivo main
# ===========================================================================

# Region -  Importaciones de archivos o librerias
from controller.Log import Log
from controller.Impresor import Impresor
from controller.Orquestador import Orquestador
from controller.utils.DataBase import DataBaseRPA
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
def main():
    try: 
        consola.imprimirInicio("Nombre de la Automatización")
        logger.registroInicioProcesos()
        logger.registrarLogProceso("Inicio de ejecución del proceso")
        
        # Region - Cuerpo de la automatización
        orq.fechaRIPS = "03-2024"
        orq.epsEjecucion = "NEPS"
        orq.relacionEnvio = "123456"
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
    main()