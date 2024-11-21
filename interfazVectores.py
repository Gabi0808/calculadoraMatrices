from PyQt5.QtWidgets import (
 QVBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QWidget,
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matrices import Matriz
from vectores import Vector
from interfazHelper import InterfazHelperVector, InterfazHelperMatriz
from visualizador import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtWidgets import (
    QWidget, QSplitter, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt

class OperacionesVectorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Vectores")
        self.setGeometry(100, 100, 500, 600)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        self.dimension_input = QLineEdit()
        self.vector_inputs = []
        self.escalar_inputs = []
        self.resultado_texto = None
        self.contenedor_vectores_layout = None

        contenedor_layout, self.contenedor_vectores_layout, self.contenedor_botones_layout = InterfazHelperVector.crear_layout_vectores(
            n_input=self.dimension_input,
            ingresar_dimension_callback=lambda: InterfazHelperVector.ingresar_vectores(dimension_input=self.dimension_input,
                                                                        vector_inputs=self.vector_inputs,
                                                                        escalar_inputs=self.escalar_inputs,
                                                                        contenedor_vectores_layout=self.contenedor_vectores_layout,
                                                                        contenedor_botones_layout=self.contenedor_botones_layout,
                                                                        ejecutar_callback=self.ejecutar_operacion
            )
        )

        self.main_layout.addLayout(contenedor_layout)
                
    def ejecutar_operacion(self):
        try:
            lista_vectores = InterfazHelperVector.leer_entrada_vectores_escalares(self.vector_inputs, self.escalar_inputs)
            if not lista_vectores:
                return 
            
            resultado, pasos = Vector.sumar_vectores(*lista_vectores)
            
            InterfazHelperMatriz.limpiar_resultados_texto(self.resultado_texto, self.main_layout)

            self.resultado_texto = InterfazHelperMatriz.mostrar_resultados(pasos)

            self.main_layout.addWidget(self.resultado_texto)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class ProductoVectorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Producto de Vector Fila por Vector Columna")
        self.setGeometry(100, 100, 500, 400)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.dimension_input = QLineEdit()
        self.vector_fila_inputs = [] 
        self.vector_columna_inputs = []
        self.escalares_inputs = []
        self.resultados_texto = None

        contenedor_layout, self.contenedor_vectores_layout, self.contenedor_botones_layout = InterfazHelperVector.crear_layout_vectores(
            n_input=self.dimension_input,
            ingresar_dimension_callback=self.ingresar_vectores_fila_columna
        )
        
        self.main_layout.addLayout(contenedor_layout)

    def ingresar_vectores_fila_columna(self):

        InterfazHelperVector.limpiar_entradas_vectores(self.vector_columna_inputs, self.escalares_inputs, self.contenedor_vectores_layout)        
        InterfazHelperVector.limpiar_entradas_vectores(self.vector_fila_inputs, self.escalares_inputs, self.contenedor_vectores_layout)        

        

        n = InterfazHelperVector.leer_entrada_dimension_vector(self.dimension_input)

        if n is None:
                return

        InterfazHelperVector.agregar_campo_vector(self.vector_fila_inputs, self.escalares_inputs, self.contenedor_vectores_layout, n, orientacion="horizontal")
        InterfazHelperVector.agregar_campo_vector(self.vector_columna_inputs, self.escalares_inputs, self.contenedor_vectores_layout, n, orientacion="vertical")

        if self.contenedor_botones_layout.count() == 0:
            ejecutar_btn = QPushButton("Calcular producto")
            ejecutar_btn.clicked.connect(self.calcular_producto)
            self.contenedor_botones_layout.addWidget(ejecutar_btn)
    
    def procesar_entrada_vectores(self):
        try:
            
            valores_escalares = [escalar[0][1] for escalar in self.escalares_inputs]
            vector_fila_obj = InterfazHelperVector.procesar_entrada(self.vector_fila_inputs, [valores_escalares[0]], "horizontal")[0]
            vector_columna_obj = InterfazHelperVector.procesar_entrada(self.vector_columna_inputs, [valores_escalares[1]], "vertical")[0]
            
            return vector_fila_obj, vector_columna_obj

        except ValueError as e:
            QMessageBox.critical(self, "Error al procesar entradas", str(e))
            return []

    def calcular_producto(self):
        try:
        
            vector_fila_obj, vector_columna_obj = self.procesar_entrada_vectores()
            
            resultado, pasos = vector_fila_obj.producto_vector_fila_por_vector_columna(vector_columna_obj)

            InterfazHelperMatriz.limpiar_resultados_texto(self.resultados_texto, self.main_layout)

            self.resultados_texto = InterfazHelperMatriz.mostrar_resultados(f"{pasos}\nResultado del producto: {resultado}")

            self.main_layout.addWidget(self.resultados_texto)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))