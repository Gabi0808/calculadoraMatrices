import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QMainWindow, QWidget, QTabWidget, QDockWidget, QToolBar,
    QStackedWidget, QAction
)
from PyQt5.QtCore import Qt

from interfazMatrices import (IngresarMatrizDialog, OperacionesVectorDialog, ProductoVectorDialog, MultiplicacionMatrizVectorDialog,
                              OperacionesMatrizDialog, MultiplicacionMatricesDialog, TranspuestaDialog, DeterminanteDialog,
                              CramerDialog, InversaTab)
from interfazAnalisisNumerico import BiseccionTab, NewtonRaphsonTab, FalsaPosicionTab, SecanteTab
from interfazHelper import AnimatedButton

def apply_stylesheet(app, style_path):
    with open(style_path, "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)

def convert_buttons(widget):
    # Convierte cada QPushButton en un AnimatedButton
    for child in widget.findChildren(QPushButton):
        animated_button = AnimatedButton(child.text())
        animated_button.setGeometry(child.geometry())
        animated_button.setParent(child.parent())
        child.deleteLater()

class MatricesScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.cerrar_pestana)

        self.boton_panel = QWidget()
        self.boton_layout = QVBoxLayout(self.boton_panel)
        
        self.crear_boton("Eliminación Gauss-Jordan (Matriz Cuadrada)", IngresarMatrizDialog, {'rectangular': False})
        self.crear_boton("Eliminación Gauss-Jordan (Matriz Rectangular)", IngresarMatrizDialog, {'rectangular': True})
        self.crear_boton("Operaciones con Vectores", OperacionesVectorDialog)
        self.crear_boton("Producto de Vector Fila por Vector Columna", ProductoVectorDialog)
        self.crear_boton("Multiplicación de Matriz por Vector", MultiplicacionMatrizVectorDialog)
        self.crear_boton("Operaciones con Matrices", OperacionesMatrizDialog)
        self.crear_boton("Multiplicar Matrices", MultiplicacionMatricesDialog)
        self.crear_boton("Transponer Matriz", TranspuestaDialog)
        self.crear_boton("Calcular Determinante", DeterminanteDialog)
        self.crear_boton("Regla de Cramer", CramerDialog)
        self.crear_boton("Matriz Inversa", InversaTab)
        
        self.boton_layout.addStretch()
        self.boton_panel.setLayout(self.boton_layout)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)

    def crear_boton(self, texto, tab_clase, parametros=None):
        boton = QPushButton(texto)
        boton.clicked.connect(lambda: self.agregar_pestana(tab_clase, texto, parametros))
        self.boton_layout.addWidget(boton)

    def agregar_pestana(self, tab_clase, titulo, parametros=None):
        if parametros:
            nueva_pestaña = tab_clase(**parametros)
        else:
            nueva_pestaña = tab_clase()
        
        nueva_index = self.tab_widget.addTab(nueva_pestaña, titulo)
    
        self.tab_widget.setCurrentIndex(nueva_index)

    def cerrar_pestana(self, index):
        self.tab_widget.removeTab(index)

class AnalisisNumericoScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.cerrar_pestana)

        self.boton_panel = QWidget()
        self.boton_layout = QVBoxLayout(self.boton_panel)
        
        self.crear_boton("Método de Bisección", BiseccionTab)
        self.crear_boton("Método Newton-Raphson", NewtonRaphsonTab)
        self.crear_boton("Método de Falsa Posición", FalsaPosicionTab)
        self.crear_boton("Método de Secante", SecanteTab)
        
        self.boton_layout.addStretch()
        self.boton_panel.setLayout(self.boton_layout)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)

    def crear_boton(self, texto, tab_clase):
        boton = QPushButton(texto)
        boton.clicked.connect(lambda: self.agregar_pestana(tab_clase, texto))
        self.boton_layout.addWidget(boton)

    def agregar_pestana(self, tab_clase, titulo):
        nueva_pestaña = tab_clase()
        nueva_index = self.tab_widget.addTab(nueva_pestaña, titulo)
        self.tab_widget.setCurrentIndex(nueva_index)

    def cerrar_pestana(self, index):
        self.tab_widget.removeTab(index)

class MenuPrincipal(QWidget):
    def __init__(self, cambiar_a_matrices, cambiar_a_analisis_numerico):
        super().__init__()
        self.cambiar_a_matrices = cambiar_a_matrices
        self.cambiar_a_analisis_numerico = cambiar_a_analisis_numerico

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        titulo = QLabel("Menú Principal")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        boton_matrices = QPushButton("Matrices")
        boton_matrices.clicked.connect(self.cambiar_a_matrices)
        layout.addWidget(boton_matrices)

        boton_analisis_numerico = QPushButton("Análisis Numérico")
        boton_analisis_numerico.clicked.connect(self.cambiar_a_analisis_numerico)
        layout.addWidget(boton_analisis_numerico)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Álgebra")
        self.setGeometry(100, 100, 600, 400)
        self.resize(1700, 800)

        convert_buttons(self)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.menu_principal = MenuPrincipal(
            cambiar_a_matrices=self.mostrar_matrices,
            cambiar_a_analisis_numerico=self.mostrar_analisis_numerico
        )
        self.stacked_widget.addWidget(self.menu_principal)

        self.matrices_screen = MatricesScreen()
        self.stacked_widget.addWidget(self.matrices_screen)

        self.analisis_numerico_screen = AnalisisNumericoScreen()
        self.stacked_widget.addWidget(self.analisis_numerico_screen)

        self.dock_boton_panel = QDockWidget("Panel de Opciones", self)
        self.dock_boton_panel.setWidget(self.matrices_screen.boton_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_boton_panel)

        self.dock_boton_panel.setVisible(False)

        self.stacked_widget.setCurrentWidget(self.menu_principal)

        self.tool_bar = QToolBar("Navegación")
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)
        
        self.boton_volver = QAction("⬅ Volver", self)
        self.boton_volver.triggered.connect(self.mostrar_menu_principal)
        self.tool_bar.addAction(self.boton_volver)

        self.boton_volver.setVisible(False)

    def mostrar_menu_principal(self):

        self.stacked_widget.setCurrentWidget(self.menu_principal)
        self.boton_volver.setVisible(False)
        self.dock_boton_panel.setVisible(False)

    def mostrar_matrices(self):

        self.stacked_widget.setCurrentWidget(self.matrices_screen)
        self.boton_volver.setVisible(True)
        self.dock_boton_panel.setWidget(self.matrices_screen.boton_panel)
        self.dock_boton_panel.setVisible(True)

    def mostrar_analisis_numerico(self):

        self.stacked_widget.setCurrentWidget(self.analisis_numerico_screen)
        self.boton_volver.setVisible(True)
        self.dock_boton_panel.setWidget(self.analisis_numerico_screen.boton_panel)
        self.dock_boton_panel.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, "themes.qss")
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
