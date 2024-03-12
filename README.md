# Zentria Carga de Soportes a SFTP

> ## Necesidad
>
> Crear una herramienta automatizada, capáz de cargar archivos relacionados a un número de relación de envío al SFTP de la clinica Zentria, sede Avidanti - Santa Marta.
>
> ## Solución
>
> Para dar solución a esta necesidad, se ha implementando un desarrollo en Python, utilizando la herramienta [Paramiko](https://docs.paramiko.org/en/3.4/api/sftp.html), mediante esta libreria podremos gestionar los recursos del SFTP, haciendo loguin en el mismo.
>
> Para implementar esta solución, la automatización necesitará recibir 3 parametros por argumentos al momento de su ejecución, estos son:
>
> * **Fecha RIPS (str):** Fecha de la generación de los RIPS, deberá coincidir con la fecha en la que se guardará la carpeta de relación de envío en la ruta de RIPS.
> * **EPS Ejecución ():** Nombre de la EPS a la que hace referencia el proceso de ejecución.
> * **Número de relación de envío (str || int):** Número de la relación de envío generado en GomediSys, que esta vinculado directamente a la generación de RIPS.

## Comentarios útiles para los procesos de automatización

### Comando para conversión de archivo *".py"* a ejecutable *".exe"*

Comando base para conversión a ejectutable:

* ***py -m PyInstaller  --icon="ruta-absoluta-archivo-ico" ruta-abosulta-main-proyecto***

Banderas de comando para ejecutable:

* **--onefile** Crea el ejecutable en un solo archivo comprimido que lleva el nombre del archivo main pasado, con extensión .exe
* **--windowed** Habilita una ventana de CMD durante la ejecución del programa la cual puede servir como depurador de los print dejados en los archivos **".py"**

Cabe resaltar que se debe tener instalada la libreria **Pyinstaller** antes de realizar este paso. **(pip install pyinstaller)**

## Librerias usadas en este proyecto - Automatización.

La siguiente es la lista completa de librerias o paquetes usados en la creación de esta solución.

* [Paramiko](https://docs.paramiko.org/en/3.4/api/sftp.html) (pip install paramiko) ***[Para configuración de conexión a SFTP]***
* [PyOdbc](https://pypi.org/project/pyodbc/)(pip install pyodbc) ***[Para manejo de base de datos SQL Server, también puede manejar otros moteres, pero con instancias premium]***
* [Fernet](https://cryptography.io/en/latest/fernet/) (pip install cryptography) ***[Para manejo de elementos encryptados, cómo datos sensibles]***
