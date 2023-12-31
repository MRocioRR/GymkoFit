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


#-------------------------AYUDA DE USO APLICACION------------------------------------------
class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Ayuda')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        label = QLabel('''
                        ¡Bienvenido a Gymkofit, tu compañero de entrenamiento personalizado
                         en línea! Nuestra aplicación web está diseñada para ayudarte a llevar
                         un control efectivo de tus rutinas y alcanzar tus objetivos de
                          acondicionamiento físico de manera óptima. Sabemos que cada persona es única,
                         por lo que hemos desarrollado un sistema inteligente que se adapta a tu estado 
                         físico individual y te proporciona recomendaciones personalizadas para lograr
                         resultados tangibles. 
                         Ya sea que desees perder peso, mejorar tu rendimiento físico, aumentar tu masa
                         muscular o simplemente mantener una buena salud física, Gymkofit está aquí
                         para ayudarte en cada paso del camino. Nuestra plataforma te permite crear
                         rutinas de entrenamiento adecuadas a tus necesidades y preferencias, y te
                         ofrece un seguimiento detallado de tu progreso para que puedas visualizar
                         tus avances.
                         Ya sea que desees perder peso, mejorar tu rendimiento físico, aumentar tu masa
                         muscular o simplemente mantener una buena salud física, Gymkofit está aquí para
                         ayudarte en cada paso del camino. Nuestra plataforma te permite crear rutinas de
                         entrenamiento adecuadas a tus necesidades y preferencias, y te ofrece un seguimiento
                         detallado de tu progreso para que puedas visualizar tus avances.
                         No importa cuál sea tu nivel de condición física actual, Gymkofit te brinda las
                         herramientas necesarias para alcanzar tus metas de manera segura y eficiente.
                         ¡Prepárate para descubrir una nueva forma de entrenar y maximizar tu potencial!
                         Únete a nosotros hoy mismo y comienza a hacer realidad tus sueños de
                         acondicionamiento físico con Gymkofit.
                         
                         
                         El usuario que utilize la aplicación debe introdicir su ID, que es proporcionado
                         por el gimnasio, con el cual todos sus datos van a quedar vinculados.

                         Después introducirá Nombre y Apellidos en los campos que indica la aplicación. De 
                         esta forma la información asociada a un ID queda también asociada a una persona concreta.

                         También será requerido Edad, Peso y Altura. Donde la edad debe ser introducida en 
                         Kilogramos y la altura en centimetros, y por supuesto todo ello en números.

                         Finalemte, los desplegables de Género, Objetivo Físico, Actividad Física y 
                         Complexión Física deben ser elegidos de manera que se ajusten lo mejor posible a cada
                         usuario.

                         Tenga en cuenta que esta información debe ser lo más real posible ya que será utilizada con
                         el fin de generar la rutina de ejercicios ideal para el usuario. Si los datos no son precisos, 
                         entonces la rutina puede ser contraproducente para el usuario.

                         Cuando todos estos campos han sido rellenados pulse el boton Insertar para insertarlos
                         en la base de datos. Si se ha confundido en algún campo puede pulsar en Cargar CSV, donde verá
                         todos los registros, seleccione el que desee eliminar y pulse el boton Eliminar.
                         

                         Esencialmente esto es todo lo que necesita saber para utilizar la aplicación. 
                         ¡¡Disfrute de la experiencia GymkoFit!!
                            ''')
        layout.addWidget(label)

        close_button = QPushButton('Cerrar')
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

#----------------------------FIN AYUDA APLICACIÓN-------------------------------------------------------------------


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
        self.lblPesoDiario = QLabel("Peso Diario:")
        self.txtPesoDiario = QLineEdit()
        self.txtPesoDiario.setPlaceholderText("Peso diario en Kg.")
        
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
        
        help_button = QPushButton('Ayuda')
        help_button.clicked.connect(self.open_help_window)
        
        # Acciones
        hbx = QHBoxLayout()
        hbx.addWidget(btnCargarCSV)
        hbx.addWidget(btnInsertar)
        hbx.addWidget(btnEliminar)
        hbx.addWidget(help_button)

        vbx = QVBoxLayout()
        vbx.addLayout(grid)
        vbx.addLayout(hbx)
        vbx.setAlignment(Qt.AlignTop)
        vbx.addWidget(self.table)
        
        # Título e Icono app
        self.setWindowTitle("GymkoFit - La meta eres tú")
        self.setWindowIcon(QtGui.QIcon(r'img\gymkofit.png'))
        self.resize(362, 320)
        self.setLayout(vbx)
        self.cargarDatosDesdeCSV(FileHandler.createCSVIfNotExisting(self.csvPath, ",".join(self.mandatoryColumns)))
            
    def open_help_window(self):
        # Boton ayuda.
        self.help_window = HelpWindow()
        self.help_window.show()
        
    def readNewCSV(self):
        # Acción de cargar los registos de ejemplo definido más abajo.
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
                    
    def eliminarDatos(self):
        # Acción de eliminar registros        
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
    

if __name__ == '__main__':
    # Método principal y ejecución de la aplicación:
    app = QApplication(sys.argv)
    window = Leccion()
    window.show()
    sys.exit(app.exec_())