# Proyecto: Gymkofit
# Este código es una aplicación de escritorio desarrollada 
# con PyQt5 para interactuar con una base de datos SQLite. 

# Importación de las librerías necesarias:
import sys

from PyQt5.QtSql import *
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout

# ---------------------------- APLICACION -------------------------------------------------

# Definición de la clase Leccion que hereda de QWidget:
class Leccion(QWidget):
    def __init__(self, parent=None):
        super(Leccion, self).__init__(parent)

        # Desarrollo de la tabla
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(['ID', 'NOMBRE', 'APELLIDO',
                                              'PESO', 'RUTINA', 'ACTIVIDAD', 'GENERO'])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Configuración de la interfaz de usuario en el constructor de la clase:
        # Variables que almacenarán los datos
        self.lblID = QLabel("ID:")
        self.txtID = QLineEdit()
        self.txtID.setPlaceholderText("Numero identificador único (Usuario Gym)")

        self.lblName = QLabel("Nombre:")
        self.txtName = QLineEdit()
        self.txtName.setPlaceholderText("Nombre de la persona")

        self.lblApellido = QLabel("Primer Apellido:")
        self.txtApellido = QLineEdit()
        self.txtApellido.setPlaceholderText("Primer Apellido de la persona")
        
        self.lblPeso = QLabel("Peso:")
        self.txtPeso = QLineEdit()
        self.txtPeso.setPlaceholderText("Control peso semanal (Kg.)")
        
        self.lblRutina = QLabel("Rutina:")
        self.txtRutina = QLineEdit()
        self.txtRutina.setPlaceholderText("Rutina Generada por la app (Valor devuelto)")
        
        self.lblActividad = QLabel("Actividad:")
        self.txtActividad = QLineEdit()
        self.txtActividad.setPlaceholderText("Nivel de actividad semanal (Sedentario - Moderado - Activo)")
        
        self.lblGenero = QLabel("Genero:")
        self.txtGenero = QLineEdit()
        self.txtGenero.setPlaceholderText("Genero que se considera (Masculino - Femenino - No Binario)")
        
        # Desarrollo de widgets
        grid = QGridLayout()
        grid.addWidget(self.lblID, 0, 0)
        grid.addWidget(self.txtID, 0, 1)
        grid.addWidget(self.lblName, 1, 0)
        grid.addWidget(self.txtName, 1, 1)
        grid.addWidget(self.lblApellido, 2, 0)
        grid.addWidget(self.txtApellido, 2, 1)
        grid.addWidget(self.lblPeso, 3, 0)
        grid.addWidget(self.txtPeso, 3, 1)
        grid.addWidget(self.lblRutina, 4, 0)
        grid.addWidget(self.txtRutina, 4, 1)
        grid.addWidget(self.lblActividad, 5, 0)
        grid.addWidget(self.txtActividad, 5, 1)
        grid.addWidget(self.lblGenero, 6, 0)
        grid.addWidget(self.txtGenero, 6, 1)

        # Botones
        btnCargar = QPushButton('Cargar Datos')
        btnCargar.clicked.connect(self.cargarDatos)
        #btnCargar.setStyleSheet("backgroud-color: blue; color: black;")
        
        btnInsertar = QPushButton('Insertar')
        btnInsertar.clicked.connect(self.insertarDatos)
        #btnInsertar.setStyleSheet("backgroud-color: green; color: black;")
        
        btnEliminar = QPushButton('Eliminar')
        btnEliminar.clicked.connect(self.eliminarDatos)
        #btnEliminar.setStyleSheet("backgroud-color: red; color: black;")
        
        # Acciones
        hbx = QHBoxLayout()
        hbx.addWidget(btnCargar)
        hbx.addWidget(btnInsertar)
        hbx.addWidget(btnEliminar)

        vbx = QVBoxLayout()
        vbx.addLayout(grid)
        vbx.addLayout(hbx)
        vbx.setAlignment(Qt.AlignTop)
        vbx.addWidget(self.table)

        # Título e Icono app
        ## PyQT :: SQLite Data Access
        self.setWindowTitle("GymkoFit - La meta eres tú")
        self.setWindowIcon(QtGui.QIcon('..\img\gymkofit.png'))
        self.resize(362, 320)
        self.setLayout(vbx)

    # Definición de métodos de acción para interactuar con la base de datos:
    # Acción de cargar los registos de ejemplo definido más abajo.
    def cargarDatos(self, event):
        index = 0
        query = QSqlQuery()
        query.exec_("select * from person")

        while query.next():
            ids = query.value(0)
            nombre = query.value(1)
            apellido = query.value(2)
            peso = query.value(3)
            rutina = query.value(4)
            actividad = query.value(5)
            genero = query.value(6)

            self.table.setRowCount(index + 1)
            self.table.setItem(index, 0, QTableWidgetItem(str(ids)))
            self.table.setItem(index, 1, QTableWidgetItem(nombre))
            self.table.setItem(index, 2, QTableWidgetItem(apellido))
            self.table.setItem(index, 3, QTableWidgetItem(str(peso)))
            self.table.setItem(index, 4, QTableWidgetItem(str(rutina)))
            self.table.setItem(index, 5, QTableWidgetItem(actividad))
            self.table.setItem(index, 6, QTableWidgetItem(genero))

            index += 1
    
    
    # Acción de insertar nuevos registros
    def insertarDatos(self, event):
        ids = int(self.txtID.text())
        nombre = self.txtName.text()
        apellido = self.txtApellido.text()
        peso = int(self.txtPeso.text())
        rutina = int(self.txtRutina.text())
        actividad = self.txtActividad.text()
        genero = self.txtGenero.text()

        query = QSqlQuery()
        query.exec_("insert into person values({0}, '{1}', '{2}','{3}','{4}','{5}', '{6}')".format(ids, nombre, apellido, peso, rutina, actividad, genero))
    
    
    # Acción de eliminar registros
    def eliminarDatos(self, event):
        selected = self.table.currentIndex()
        if not selected.isValid() or len(self.table.selectedItems()) < 1:
            return

        ids = self.table.selectedItems()[0]
        query = QSqlQuery()
        query.exec_("delete from person where id = " + ids.text())

        self.table.removeRow(selected.row())
        self.table.setCurrentIndex(QModelIndex())
        
    # Métodos auxiliares para la conexión y creación de la base de datos:    
    # Acción de conectarse a una BD (Pendiente de mejora)
    def db_connect(self, filename, server):
        db = QSqlDatabase.addDatabase(server)
        db.setDatabaseName(filename)
        if not db.open():
            QMessageBox.critical(None, "Nose puede abrir la base de datos (futura versión)",
                    "Nose pudo establecer una conexión con la base de datos.\n"
                    "Este ejercicio necesita compatibilidad con SQLite."
                    "Continuación del ejercicio anterior en Tkinter.\n\n"
                    "Haga clic en Cancelar para salir.", QMessageBox.Cancel)
            return False
        return True
       
    # Creamos e insertamos una BD de ejemplo.    
    def db_create(self):
        query = QSqlQuery()
        query.exec_("create table person(id int primary key, "
                    "firstname varchar(20), lastname varchar(20), peso int, rutina int, actividad varchar(20), genero varchar(20))")
        query.exec_("insert into person values(101, 'Rocio', 'Roldan', 60, 65, 'Activo', 'Femenino')")
        query.exec_("insert into person values(102, 'Roberto', 'Vargas', 80, 90, 'Sedentario','Masculino')")
        query.exec_("insert into person values(103, 'Javier', 'Castillo', 84, 90, 'Sedentario','Masculino')")
        query.exec_("insert into person values(104, 'Alberto', 'Quero', 90, 105, 'Activo', 'Masculino')")
        query.exec_("insert into person values(105, 'Joel', 'Rodriguez', 70, 80, 'Moderado', 'No Binario')")
        query.exec_("insert into person values(106, 'Noelia', 'Navarro', 60, 65, 'Moderado', 'Femenino')")

    def init(self, filename, server):
        import os
        if not os.path.exists(filename):
            self.db_connect(filename, server)
            self.db_create()
        else:
            self.db_connect(filename, server)

# Método principal y ejecución de la aplicación:
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ejm = Leccion()
    ejm.init('datafile', 'QSQLITE')
    ejm.show()
    sys.exit(app.exec_())
