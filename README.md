# GymkoFit

**Este código es una aplicación de escritorio desarrollada con PyQt5 para interactuar con una base de datos SQLite.**

Aquí tienes una descripción paso a paso del código:

1. Importación de las librerías necesarias:

- *sys*: Proporciona funciones y variables que interactúan con el intérprete de Python.
- *QSql* (parte de PyQt5.QtSql): Proporciona clases para trabajar con bases de datos.
- *Qt, QModelIndex* (parte de PyQt5.QtCore): Proporciona clases centrales para la funcionalidad principal de PyQt5.
- *QtGui* (parte de PyQt5): Proporciona clases para ventanas, gráficos, fuentes y otros elementos de la interfaz de usuario.
- *QWidget, QApplication, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout* (parte de PyQt5.QtWidgets): Proporciona clases para crear interfaces de usuario.

2. Definición de la clase Leccion que hereda de QWidget:

- *__init__(self, parent=None)*: Constructor de la clase. Se inicializan los widgets, se configuran las propiedades de la ventana y se conectan las señales con los slots correspondientes.

3. Configuración de la interfaz de usuario en el constructor de la clase:

- Se crean los widgets necesarios, como la tabla *(QTableWidget)* y los campos de entrada *(QLineEdit)* y etiquetas *(QLabel)*.
- Se establecen las propiedades de los widgets, como el número de columnas y las etiquetas de la tabla, el texto de marcador de posición en los campos de entrada, etc.
- Se crean y configuran los botones *(QPushButton)* para cargar datos, insertar registros y eliminar registros.
- Se organizan los widgets en una disposición de cuadrícula *(QGridLayout)* y una disposición horizontal *(QHBoxLayout)*.
- Se establece la disposición vertical *(QVBoxLayout)* principal de la ventana y se agregan los widgets a ella.
- Se configuran el título y el icono de la aplicación.

4. Definición de métodos de acción para interactuar con la base de datos:

- *cargarDatos(self, event)*: Recupera los registros de la base de datos y los muestra en la tabla.
- *insertarDatos(self, event)*: Inserta un nuevo registro en la base de datos utilizando los valores ingresados en los campos de entrada.
- *eliminarDatos(self, event)*: Elimina el registro seleccionado de la base de datos y de la tabla.

5. Métodos auxiliares para la conexión y creación de la base de datos:

- *db_connect(self, filename, server)*: Conecta con la base de datos SQLite utilizando el nombre de archivo proporcionado.
- *db_create(self)*: Crea una tabla de ejemplo en la base de datos y agrega algunos registros de muestra.

4. Método principal y ejecución de la aplicación:

- *if __name__ == '__main__'*: Verifica si el archivo se está ejecutando directamente.
- *app = QApplication(sys.argv)*: Crea una instancia de la aplicación Qt.
- *ejm = Leccion()*: Crea una instancia de la clase Leccion.
- *ejm.init('datafile', 'QSQLITE')*: Inicializa la base de datos y crea la tabla de ejemplo si no existe.
