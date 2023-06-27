# Proyecto: Gymkofit
# Este código es una aplicación de escritorio desarrollada 
# con PyQt5 para interactuar con una base de datos SQLite. 

# Importación de las librerías necesarias:
import sys

# Own modules and dependencies
from file_handler import FileHandler

from PyQt5.QtSql import *
from PyQt5.QtCore import (Qt, QDate)
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QPushButton,
    QTableWidget, QMessageBox, QHBoxLayout, QLineEdit, 
    QLabel, QGridLayout , QComboBox, QFileDialog,
    QTableWidgetItem, QDateEdit, QMainWindow, QAction)

from pandas import concat, DataFrame


# ---------------------------- APLICACION -------------------------------------------------

# Definición de la clase Leccion que hereda de QWidget:
class Leccion(QWidget):
    csvPath:str = "usuarios.csv"
    mandatoryColumns:list = [
        'ID', 
        'Nombre', 
        'P_Apellido', 
        'S_Apellido', 
        'Edad',
        'Peso',
        'Altura',
        'Genero', 
        'Obj_Fisico',
        'Act_Fisica',
        'Complexion_Fisica',
        'Fecha'       
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent)
                    
        # Desarrollo de la tabla
        self.table = QTableWidget(0, 12)
        self.table.setHorizontalHeaderLabels(self.mandatoryColumns)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Configuración de la interfaz de usuario en el constructor de la clase:
        # Variables que almacenarán los datos
        self.lblID = QLabel("DNI/NIE:")
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
        
        self.lblFecha = QLabel("Fecha:")
        self.txtFecha = QDateEdit()
        self.txtFecha.setDisplayFormat("yyyy-MM-dd")
        self.txtFecha.setSpecialValueText("Fecha. Indica la fecha actual")
        self.txtFecha.setDate(QDate.currentDate())
        
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
        self.Genero.addItems([
            'Femenino',
            'Masculino',
            'No Binario'
            ])
        grid.addWidget(self.lblGenero, 7, 0)
        grid.addWidget(self.Genero, 7, 1)
        self.ObjFisico = QComboBox()
        self.ObjFisico.addItems([
            'Ganar masa muscular',
            'Perder peso', 
            'Definición',
            'Salud',
            'Rendimiento'
            ])
        grid.addWidget(self.lblObjFisico, 8, 0)
        grid.addWidget(self.ObjFisico, 8, 1)  
        self.Actividad = QComboBox()
        self.Actividad.addItems([
            'Muy sedentario (Más de 12 horas sin act.física)',
            'Sedentario (Entre 12 - 8 horas sin act.física)',
            'Medianamente activo (1-2 días alguna act.física)',
            'Activo (Entre 2-3 días alguna act.física)',
            'Muy activo (Más de 3 días alguna act.física)',
            'Alto rendimiento (Competiciones)'
            ])
        grid.addWidget(self.lblActividad, 9, 0)
        grid.addWidget(self.Actividad, 9, 1)     
        self.CompFisica = QComboBox()
        self.CompFisica.addItems([
            'Endomorfo (constitución corporal gruesa)',
            'Mesomorfo (constitución corporal atlético y musculoso)',
            'Ectomorfo (constitución corporal delgada)'
            ])
        grid.addWidget(self.lblCompFisica, 10, 0)
        grid.addWidget(self.CompFisica, 10, 1)  
        grid.addWidget(self.lblFecha, 11, 0)
        grid.addWidget(self.txtFecha, 11, 1)
            
        # Botones
        btnCargarCSV = QPushButton('Cargar CSV distinto')
        btnCargarCSV.clicked.connect(self.readNewCSV)
        
        btnInsertar = QPushButton('Insertar')
        btnInsertar.clicked.connect(self.insertarDatos)
        
        btnEliminar = QPushButton('Eliminar')
        btnEliminar.clicked.connect(self.eliminarDatos)
        
        # Acciones
        hbx = QHBoxLayout()
        hbx.addWidget(btnCargarCSV)
        hbx.addWidget(btnInsertar)
        hbx.addWidget(btnEliminar)

        vbx = QVBoxLayout()
        vbx.addLayout(grid)
        vbx.addLayout(hbx)
        vbx.setAlignment(Qt.AlignTop)
        vbx.addWidget(self.table)
        
        # Título e Icono app
        self.setWindowTitle("GymkoFit - La meta eres tú")
        self.setWindowIcon(QtGui.QIcon(r'img\gymkofit.png'))
        # TODO: queremos implementar esto o not needed?
        # self.init("usuarios.db", "QSQLITE")
        self.resize(362, 320)
        self.setLayout(vbx)
        self.cargarDatosDesdeCSV(FileHandler.createCSVIfNotExisting(self.csvPath, ",".join(self.mandatoryColumns)))
        
        
    # Definición de métodos de acción para interactuar con la base de datos:
    # Acción de cargar los registos de ejemplo definido más abajo.
    def readNewCSV(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV", "", "Archivos CSV (*.csv)")
        self.cargarDatosDesdeCSV(filename)        

    def cargarDatosDesdeCSV(self, filename:str):
        if filename:
            try:
                self.readData = FileHandler.readCSV(filename, self.mandatoryColumns)
                self.displayData()
                self.table.show()
                self.csvPath = filename
            except Exception as error:
                QMessageBox.critical(self, "Cargando datos", f"{error}")
                
    def displayData(self) -> None:
        """Dado cierto DataFrame, muestra los datos del mismo en la QTableView ya instanciada e inicializada."""
        self.table.setRowCount(self.readData.shape[0])
        for rowIndex in range(self.readData.shape[0]):
            for columnIndex in range(self.readData.shape[1]):
                item = QTableWidgetItem(str(self.readData.iloc[rowIndex, columnIndex]))
                self.table.setItem(rowIndex, columnIndex, item)        
                    
    # Acción de eliminar registros
    def eliminarDatos(self):
        # Tenemos seteado SingleSelection        
        selected_row = self.table.currentRow()
        print(selected_row)
        if selected_row >= 0:
            try:
                self.readData = self.readData.drop(index=selected_row)
                self.table.removeRow(selected_row)
                self.readData.to_csv(self.csvPath, index=False)
                self.table.show()
                QMessageBox.information(self, "Eliminar", "Registro eliminado correctamente.")
            except Exception as error:
                QMessageBox.critical(self, "Error al eliminar", f"No se pudo eliminar correctamente: {error}")
        else:
            QMessageBox.warning(self, "Eliminar", "Seleccione una fila para eliminar.")
            
    def insertarDatos(self) -> None:
        try:
            fecha = self.txtFecha.date().toString("yyyy-MM-dd")
            valuesToAdd = (
                self.txtID.text(),
                self.txtName.text(),
                self.txtPrimerApellido.text(),
                self.txtSegundoApellido.text(),
                int(self.txtEdad.text()),
                float(self.txtPeso.text()),
                int(self.txtAltura.text()),
                self.Genero.currentText(),
                self.ObjFisico.currentText(),
                self.Actividad.currentText(),
                self.CompFisica.currentText(), 
                fecha   
            )
            dataMapped = dict(zip(self.mandatoryColumns, valuesToAdd))
            # Comprueba que el ID introducido no exista
            if dataMapped["ID"] in self.readData["ID"].unique().tolist(): 
                raise ValueError()
            self.readData = concat([self.readData, DataFrame(dataMapped, index=[0])], ignore_index=True, sort=False)
            self.readData.to_csv(self.csvPath, index=False)
            QMessageBox.information(self, "Añadido", "Datos añadidos correctamente y guardados en el csv cargado " + 
                                    f"({self.csvPath}).")
        except ValueError as error:
            QMessageBox.warning(self, f"DNI/NIE ya existente", "Ya existe un usuario con este DNI/NIE.")
            QMessageBox.information(self, "Info", f"DNI: {dataMapped['ID']}, values: {self.readData['ID'].unique().tolist()}")
            return
        except Exception as error:
            QMessageBox.critical(self, "Error al añadir datos", f"{error}")
            return
        try:
            lastRow = self.readData.iloc[-1]
            self.table.setRowCount(self.table.rowCount() + 1)
            for columnIndex, value in enumerate(lastRow):
                item = QTableWidgetItem(str(value))
                self.table.setItem(self.table.rowCount() - 1, columnIndex, item)        
        except Exception as error:
            QMessageBox.warning(self, "Añadido", "Los datos fueron registrados pero no es posible visualizarlos en la tabla "\
                f"debido a un error inesperado: {error}")
                   
# TODO: si implementamos SQLite, lo metemos, por ahora commented
#     # Métodos auxiliares para la conexión y creación de la base de datos:    
#     def db_connect(self, filename, server):
#         db = QSqlDatabase.addDatabase(server)
#         db.setDatabaseName(filename)
#         if not db.open():
#             QMessageBox.critical(None, 
#                     "Nose pudo establecer una conexión con la base de datos.",
#                     "Este ejercicio necesita compatibilidad con SQLite.\n"
#                     "Haga clic en Cancelar para salir.", QMessageBox.Cancel)
#             return False
#         return True

#    # Creamos e insertamos nuevos registros
#     def db_create(self):
#         query = QSqlQuery()
#         query.exec_("create table if not exists person(id int primary key, "
#                     "primerapellido varchar(20), segundoapellido varchar(20), edad int, peso int, altura int, genero varchar(20), objfisico varchar(50), actividad varchar(50), compfisica varchar(50))")
#         if query.isActive():
#             print("Tabla creada correctamente")
#         else:
#             print("Error al crear la tabla:", query.lastError().text())
            

#     def init(self, filename, server):
#         import os
#         if not os.path.exists(filename):
#             self.db_connect(filename, server)
#             self.db_create()
#         else:
#             self.db_connect(filename, server)    
    

# Método principal y ejecución de la aplicación:
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # TODO: just if SQLite implementation in sprint
    # db = QSqlDatabase.addDatabase("QSQLITE")
    # db.setDatabaseName("usuarios.db")
    # if not db.open():
    #     QMessageBox.critical(None, "Error", "No se pudo conectar a la base de datos.")
    #     sys.exit(1)

    # query = QSqlQuery(db)
    # query.exec("CREATE TABLE IF NOT EXISTS usuarios (ID INTEGER PRIMARY KEY, Nombre TEXT, "
    #            "P_Apellido TEXT, S_Apellido TEXT, Edad INTEGER, Peso REAL, Altura INTEGER, "
    #            "Género TEXT, Objetivo_Físico TEXT, Actividad_Física TEXT, Complexión_Física TEXT)")

    window = Leccion()
    # TODO: just if SQLite implementation in sprint
    # window.db = db  # Asignar la conexión de la base de datos al objeto Leccion
    window.show()
    sys.exit(app.exec_())
