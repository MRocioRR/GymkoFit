# Proyecto: Gymkofit
# Este código es una aplicación de escritorio desarrollada 
# con PyQt5 para interactuar con una base de datos SQLite. 

# Importación de las librerías necesarias:
import sys
import csv

from PyQt5.QtSql import *
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, \
    QGridLayout , QComboBox, QFileDialog, QMainWindow


# ---------------------------- APLICACION -------------------------------------------------

# Definición de la clase Leccion que hereda de QWidget:
class Leccion(QWidget):
    def __init__(self, parent=None):
        #super(Leccion, self).__init__(parent)
        super().__init__(parent)
        
        # Desarrollo de la tabla
        self.table = QTableWidget(0, 11)
        self.table.setHorizontalHeaderLabels(['ID', 'Nombre', 'P_Apellido', 'S_Apellido',
                                              'Edad', 'Peso', 'Altura', 'Genero', 
                                              'Obj_Fisico', 'Act_Fisica', 'Complexion_Fisica'])
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

        self.lblPrimerApellido = QLabel("Primer Apellido:")
        self.txtPrimerApellido = QLineEdit()
        self.txtPrimerApellido.setPlaceholderText("Primer Apellido de la persona")
        
        self.lblSegundoApellido = QLabel("Segundo Apellido:")
        self.txtSegundoApellido = QLineEdit()
        self.txtSegundoApellido.setPlaceholderText("Segundo Apellido de la persona")
        
        self.lblEdad = QLabel("Edad:")
        self.txtEdad = QLineEdit()
        self.txtEdad.setPlaceholderText("Edad (número)")
        
        self.lblPeso = QLabel("Peso:")
        self.txtPeso = QLineEdit()
        self.txtPeso.setPlaceholderText("Control peso semanal (Kg.)(número)")
        
        self.lblAltura = QLabel("Altura:")
        self.txtAltura = QLineEdit()
        self.txtAltura.setPlaceholderText("Altura (ej. 150 cm.)(número)")   
        
        self.lblGenero = QLabel("Genero:")
        self.Genero = QComboBox()
        self.Genero.setPlaceholderText("Genero que se considera (Masculino - Femenino - No Binario)")     
        
        self.lblObjFisico = QLabel("Objetivo Físico:")
        self.ObjFisico = QComboBox()
        self.ObjFisico.setPlaceholderText("Objetivo Físico. Selecciona una opción")

        self.lblActividad = QLabel("Actividad Física:")
        self.Actividad = QComboBox()
        self.Actividad.setPlaceholderText("Nivel de actividad semanal. Selecciona una opción")

        self.lblCompFisica = QLabel("Complexión Física:")
        self.CompFisica = QComboBox()
        self.CompFisica.setPlaceholderText("Complexión Física. Selecciona una opción")
        
        
        # Desarrollo de widgets
        grid = QGridLayout()
        grid.addWidget(self.lblID, 0, 0)
        grid.addWidget(self.txtID, 0, 1)
        grid.addWidget(self.lblName, 1, 0)
        grid.addWidget(self.txtName, 1, 1)
        grid.addWidget(self.lblPrimerApellido, 2, 0)
        grid.addWidget(self.txtPrimerApellido, 2, 1)
        grid.addWidget(self.lblSegundoApellido, 3, 0)
        grid.addWidget(self.txtSegundoApellido, 3, 1)
        grid.addWidget(self.lblEdad, 4, 0)
        grid.addWidget(self.txtEdad, 4, 1)
        grid.addWidget(self.lblPeso, 5, 0)
        grid.addWidget(self.txtPeso, 5, 1)
        grid.addWidget(self.lblAltura, 6, 0)
        grid.addWidget(self.txtAltura, 6, 1)
        self.Genero = QComboBox()
        self.Genero.addItems(['Femenino'
                            , 'Masculino'
                            , 'No Binario'])
        grid.addWidget(self.lblGenero, 7, 0)
        grid.addWidget(self.Genero, 7, 1)
        self.ObjFisico = QComboBox()
        self.ObjFisico.addItems(['Ganar masa muscular'
                            , 'Perder peso'
                            , 'Definición'
                            , 'Salud'
                            , 'Rendimiento'])
        grid.addWidget(self.lblObjFisico, 8, 0)
        grid.addWidget(self.ObjFisico, 8, 1)  
        self.Actividad = QComboBox()
        self.Actividad.addItems(['Muy sedentario (Más de 12 horas sin act.física)'
                            ,'Sedentario (Entre 12 - 8 horas sin act.física)'
                            ,'Medianamente activo (1-2 días alguna act.física)' 
                            ,'Activo (Entre 2-3 días alguna act.física)'
                            ,'Muy activo (Más de 3 días alguna act.física)'
                            ,'Alto rendimiento (Competiciones)'])
        grid.addWidget(self.lblActividad, 9, 0)
        grid.addWidget(self.Actividad, 9, 1)     
        self.CompFisica = QComboBox()
        self.CompFisica.addItems(['Endomorfo (constitución corporal gruesa)'
                             , 'Mesomorfo (constitución corporal atlético y musculoso)'
                             , 'Ectomorfo (constitución corporal delgada)'])
        grid.addWidget(self.lblCompFisica, 10, 0)
        grid.addWidget(self.CompFisica, 10, 1)  

        # Botones
        #btnCargar = QPushButton('Cargar Datos')
        #btnCargar.clicked.connect(self.cargarDatos)
        #btnCargar.setStyleSheet("backgroud-color: blue; color: black;")
        btnCargarCSV = QPushButton('Cargar CSV')
        btnCargarCSV.clicked.connect(self.cargarDatosDesdeCSV)
        
        btnInsertar = QPushButton('Insertar')
        btnInsertar.clicked.connect(self.insertarDatos)
        #btnInsertar.setStyleSheet("backgroud-color: green; color: black;")
        
        btnEliminar = QPushButton('Eliminar')
        btnEliminar.clicked.connect(self.eliminarDatos)
        #btnEliminar.setStyleSheet("backgroud-color: red; color: black;")
        
        # Acciones
        hbx = QHBoxLayout()
        #hbx.addWidget(btnCargar)
        hbx.addWidget(btnCargarCSV)
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
        self.init("usuarios.db", "QSQLITE")
        self.resize(362, 320)
        self.setLayout(vbx)

    # Definición de métodos de acción para interactuar con la base de datos:
    # Acción de cargar los registos de ejemplo definido más abajo.
    def cargarDatosDesdeCSV(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV", "", "Archivos CSV (*.csv)")
        if filename:
            with open(filename, newline='') as usuarios:
                reader = csv.reader(usuarios, delimiter=',')
                primera_fila = True  # Bandera para omitir la primera fila
                for row in reader:
                    if primera_fila:
                        primera_fila = False
                        continue  # Saltar la primera fila
                
                    # Obtener los datos de cada fila del archivo CSV
                    ids = int(row[0])
                    nombre = row[1]
                    primerapellido = row[2]
                    segundoapellido = row[3]
                    edad = int(row[4])
                    peso = float(row[5])
                    altura = int(row[6])
                    genero = row[7]
                    objfisico = row[8]
                    actividad = row[9]
                    compfisica = row[10]

                    # Insertar los datos en la tabla
                    index = self.table.rowCount()
                    self.table.insertRow(index)
                    self.table.setItem(index, 0, QTableWidgetItem(str(ids)))
                    self.table.setItem(index, 1, QTableWidgetItem(nombre))
                    self.table.setItem(index, 2, QTableWidgetItem(primerapellido))
                    self.table.setItem(index, 3, QTableWidgetItem(segundoapellido))
                    self.table.setItem(index, 4, QTableWidgetItem(str(edad)))
                    self.table.setItem(index, 5, QTableWidgetItem(str(peso)))
                    self.table.setItem(index, 6, QTableWidgetItem(str(altura)))
                    self.table.setItem(index, 7, QTableWidgetItem(genero))
                    self.table.setItem(index, 8, QTableWidgetItem(objfisico))
                    self.table.setItem(index, 9, QTableWidgetItem(actividad))
                    self.table.setItem(index, 10, QTableWidgetItem(compfisica))
                    
            index += 1
            
        self.insertarDatos()
    
    # Acción de insertar nuevos registros
    def insertarDatos(self):
        ids = int(self.txtID.text())
        nombre = self.txtName.text()
        primerapellido = self.txtPrimerApellido.text()
        segundoapellido = self.txtSegundoApellido.text()
        edad = int(self.txtEdad.text())
        peso = float(self.txtPeso.text())
        altura = int(self.txtAltura.text())
        genero = self.Genero.currentText()
        objfisico = self.ObjFisico.currentText()
        actividad = self.Actividad.currentText()
        compfisica = self.CompFisica.currentText()

        index = self.table.rowCount()
        self.table.insertRow(index)
        self.table.setItem(index, 0, QTableWidgetItem(str(ids)))
        self.table.setItem(index, 1, QTableWidgetItem(nombre))
        self.table.setItem(index, 2, QTableWidgetItem(primerapellido))
        self.table.setItem(index, 3, QTableWidgetItem(segundoapellido))
        self.table.setItem(index, 4, QTableWidgetItem(str(edad)))
        self.table.setItem(index, 5, QTableWidgetItem(str(peso)))
        self.table.setItem(index, 6, QTableWidgetItem(str(altura)))
        self.table.setItem(index, 7, QTableWidgetItem(genero))
        self.table.setItem(index, 8, QTableWidgetItem(objfisico))
        self.table.setItem(index, 9, QTableWidgetItem(actividad))
        self.table.setItem(index, 10, QTableWidgetItem(compfisica))

        # Guardar el registro en la base de datos
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO usuarios (ID, Nombre, P_Apellido, S_Apellido, Edad, Peso, Altura, Genero, Objetivo_Fisico, Actividad_Fisica, Complexion_Fisica) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        
        query.addBindValue(ids)
        query.addBindValue(nombre)
        query.addBindValue(primerapellido)
        query.addBindValue(segundoapellido)
        query.addBindValue(edad)
        query.addBindValue(peso)
        query.addBindValue(altura)
        query.addBindValue(genero)
        query.addBindValue(objfisico)
        query.addBindValue(actividad)
        query.addBindValue(compfisica)
        query.exec()

        if not query.exec():
            QMessageBox.critical(self, "Error", "No se pudo insertar el registro en la base de datos.")
            self.table.removeRow(index)   
            
        
    # Acción de eliminar registros
    def eliminarDatos(self):
        selected_row = self.table.selectionModel().selectedRows()
        if selected_row:
            index = selected_row[0]
            self.table.removeRow(index.row())

            # Eliminar el registro de la base de datos
            id = int(self.table.item(index.row(), 0).text())
            query = QSqlQuery(self.db)
            query.prepare("DELETE FROM usuarios WHERE ID = ?")
            query.addBindValue(id)
            query.exec()

            QMessageBox.information(self, "Eliminar", "Registro eliminado correctamente.")
        else:
            QMessageBox.warning(self, "Eliminar", "Seleccione una fila para eliminar.")

        
    # Métodos auxiliares para la conexión y creación de la base de datos:    
    def db_connect(self, filename, server):
        db = QSqlDatabase.addDatabase(server)
        db.setDatabaseName(filename)
        if not db.open():
            QMessageBox.critical(None, 
                    "Nose pudo establecer una conexión con la base de datos.",
                    "Este ejercicio necesita compatibilidad con SQLite.\n"
                    "Haga clic en Cancelar para salir.", QMessageBox.Cancel)
            return False
        return True

   # Creamos e insertamos nuevos registros
    def db_create(self):
        query = QSqlQuery()
        query.exec_("create table if not exists person(id int primary key, "
                    "primerapellido varchar(20), segundoapellido varchar(20), edad int, peso int, altura int, genero varchar(20), objfisico varchar(50), actividad varchar(50), compfisica varchar(50))")
        if query.isActive():
            print("Tabla creada correctamente")
        else:
            print("Error al crear la tabla:", query.lastError().text())
            

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
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("usuarios.db")
    if not db.open():
        QMessageBox.critical(None, "Error", "No se pudo conectar a la base de datos.")
        sys.exit(1)

    query = QSqlQuery(db)
    query.exec("CREATE TABLE IF NOT EXISTS usuarios (ID INTEGER PRIMARY KEY, Nombre TEXT, "
               "P_Apellido TEXT, S_Apellido TEXT, Edad INTEGER, Peso REAL, Altura INTEGER, "
               "Género TEXT, Objetivo_Físico TEXT, Actividad_Física TEXT, Complexión_Física TEXT)")

    window = Leccion()
    window.db = db  # Asignar la conexión de la base de datos al objeto Leccion
    window.show()
    sys.exit(app.exec_())
