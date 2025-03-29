# Sistema Contable

Creado Por Johan Rodriguez

## Descripción

El Sistema Contable es una aplicación de escritorio desarrollada en Python utilizando PySide6 para la gestión de facturas y transacciones contables. Este sistema permite a los usuarios añadir, buscar, ver y guardar información relacionada con las transacciones de una empresa, así como gestionar clientes y empresas asociadas.

## Características

- **Añadir Transacciones**: Permite añadir nuevas transacciones con detalles como fecha, empresa, tipo de transacción, cliente, montos imponibles y exentos, entre otros.
- **Buscar Clientes**: Facilita la búsqueda de clientes asociados a una empresa.
- **Ver Facturas**: Muestra las facturas registradas y permite la gestión de archivos adjuntos.
- **Guardar Datos**: Guarda la información de las transacciones en un archivo JSON.
- **Subir Archivos**: Permite subir y gestionar archivos adjuntos a las transacciones.
- **Exportar a Excel**: Exporta los datos de las transacciones a archivos Excel.

## Requisitos

- Python 3.8 o superior
- PySide6
- json
- os
- shutil

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu_usuario/sistema-contable.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd sistema-contable
    ```
## Uso

1. Ejecuta la aplicación:
    ```bash
    python codigo/Gui_login.py
    ```
2. Utiliza la interfaz gráfica para gestionar las transacciones contables.

## Estructura del Proyecto
- `codigo/Gui_login.py`: Interfaz para ingresar los datos de inicion de sesion.
- `codigo/accounting_system.py`: Archivo principal de la aplicación.
- `codigo/factura.py`: Módulo para la gestión de facturas.
- `codigo/save_user.py`: Módulo para guardar información de usuarios.
- `codigo/client_list.py`: Módulo para la lista de clientes.
- `contribuyentes.json`: Archivo JSON con la información de contribuyentes.
- `datos_guardados.json`: Archivo JSON donde se guardan las transacciones.

## Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.

