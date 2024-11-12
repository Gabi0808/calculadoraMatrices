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
from interfazAnalisisNumerico import BiseccionTab, NewtonRaphsonTab  # Importamos el método de bisección


class MatricesScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        # Crear el QTabWidget para las pestañas
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.cerrar_pestana)

        # Crear el panel de botones en un QWidget (en lugar de QDockWidget)
        self.boton_panel = QWidget()
        self.boton_layout = QVBoxLayout(self.boton_panel)
        
        # Crear botones para diferentes funciones
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
        
        # Layout principal para la pantalla de Matrices
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)

    def crear_boton(self, texto, tab_clase, parametros=None):
        boton = QPushButton(texto)
        boton.clicked.connect(lambda: self.agregar_pestana(tab_clase, texto, parametros))
        self.boton_layout.addWidget(boton)

    def agregar_pestana(self, tab_clase, titulo, parametros=None):
        # Crear una instancia de la pestaña con parámetros si es necesario
        if parametros:
            nueva_pestaña = tab_clase(**parametros)
        else:
            nueva_pestaña = tab_clase()
        
        # Agregar la pestaña al QTabWidget con el título proporcionado
        self.tab_widget.addTab(nueva_pestaña, titulo)

    def cerrar_pestana(self, index):
        # Cerrar la pestaña en el índice especificado
        self.tab_widget.removeTab(index)


class AnalisisNumericoScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        # Crear el QTabWidget para las pestañas de métodos numéricos
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.cerrar_pestana)

        # Crear el panel de botones en un QWidget
        self.boton_panel = QWidget()
        self.boton_layout = QVBoxLayout(self.boton_panel)
        
        # Botón para el método de Bisección
        self.crear_boton("Método de Bisección", BiseccionTab)
        self.crear_boton("Método Newton-Raphson", NewtonRaphsonTab)
        
        self.boton_layout.addStretch()
        self.boton_panel.setLayout(self.boton_layout)
        
        # Layout principal para la pantalla de Análisis Numérico
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)

    def crear_boton(self, texto, tab_clase):
        boton = QPushButton(texto)
        boton.clicked.connect(lambda: self.agregar_pestana(tab_clase, texto))
        self.boton_layout.addWidget(boton)

    def agregar_pestana(self, tab_clase, titulo):
        # Crear una instancia de la pestaña
        nueva_pestaña = tab_clase()
        # Agregar la pestaña al QTabWidget con el título proporcionado
        self.tab_widget.addTab(nueva_pestaña, titulo)

    def cerrar_pestana(self, index):
        # Cerrar la pestaña en el índice especificado
        self.tab_widget.removeTab(index)


class MenuPrincipal(QWidget):
    def __init__(self, cambiar_a_matrices, cambiar_a_analisis_numerico):
        super().__init__()
        self.cambiar_a_matrices = cambiar_a_matrices
        self.cambiar_a_analisis_numerico = cambiar_a_analisis_numerico

        # Diseño del menú principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        titulo = QLabel("Menú Principal")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Botón para abrir el módulo de matrices
        boton_matrices = QPushButton("Matrices")
        boton_matrices.clicked.connect(self.cambiar_a_matrices)
        layout.addWidget(boton_matrices)

        # Botón para abrir el módulo de análisis numérico
        boton_analisis_numerico = QPushButton("Análisis Numérico")
        boton_analisis_numerico.clicked.connect(self.cambiar_a_analisis_numerico)
        layout.addWidget(boton_analisis_numerico)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Álgebra")
        self.setGeometry(100, 100, 600, 400)
        self.resize(1700, 800)

        # Crear el QStackedWidget para cambiar entre pantallas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Crear el menú principal
        self.menu_principal = MenuPrincipal(
            cambiar_a_matrices=self.mostrar_matrices,
            cambiar_a_analisis_numerico=self.mostrar_analisis_numerico
        )
        self.stacked_widget.addWidget(self.menu_principal)

        # Crear la pantalla de matrices con pestañas
        self.matrices_screen = MatricesScreen()
        self.stacked_widget.addWidget(self.matrices_screen)

        # Crear la pantalla de análisis numérico con pestañas
        self.analisis_numerico_screen = AnalisisNumericoScreen()
        self.stacked_widget.addWidget(self.analisis_numerico_screen)

        # Crear y añadir el QDockWidget con el panel de opciones
        self.dock_boton_panel = QDockWidget("Panel de Opciones", self)
        self.dock_boton_panel.setWidget(self.matrices_screen.boton_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_boton_panel)

        self.dock_boton_panel.setVisible(False)

        # Mostrar el menú principal al inicio
        self.stacked_widget.setCurrentWidget(self.menu_principal)

        # Agregar una barra de herramientas con un botón de "volver"
        self.tool_bar = QToolBar("Navegación")
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)
        
        # Agregar el botón de "volver" a la barra de herramientas
        self.boton_volver = QAction("⬅ Volver", self)
        self.boton_volver.triggered.connect(self.mostrar_menu_principal)
        self.tool_bar.addAction(self.boton_volver)

        # Ocultar el botón de "volver" cuando estamos en el menú principal
        self.boton_volver.setVisible(False)

    def mostrar_menu_principal(self):
        # Cambiar al menú principal y ocultar el botón de "volver" y el dock
        self.stacked_widget.setCurrentWidget(self.menu_principal)
        self.boton_volver.setVisible(False)
        self.dock_boton_panel.setVisible(False)

    def mostrar_matrices(self):
        # Cambiar a la pantalla de matrices y mostrar el botón de "volver"
        self.stacked_widget.setCurrentWidget(self.matrices_screen)
        self.boton_volver.setVisible(True)
        self.dock_boton_panel.setWidget(self.matrices_screen.boton_panel)
        self.dock_boton_panel.setVisible(True)

    def mostrar_analisis_numerico(self):
        # Cambiar a la pantalla de análisis numérico y mostrar el botón de "volver"
        self.stacked_widget.setCurrentWidget(self.analisis_numerico_screen)
        self.boton_volver.setVisible(True)
        self.dock_boton_panel.setWidget(self.analisis_numerico_screen.boton_panel)
        self.dock_boton_panel.setVisible(True)


# Iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
