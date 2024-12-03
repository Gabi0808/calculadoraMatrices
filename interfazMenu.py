import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QMainWindow, QWidget, QTabWidget, QDockWidget, QToolBar,
    QStackedWidget, QAction, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QIcon
from interfazMatrices import (IngresarMatrizDialog, MultiplicacionMatrizVectorDialog,
                              OperacionesMatrizDialog, MultiplicacionMatricesDialog, TranspuestaDialog, DeterminanteDialog,
                              CramerDialog, InversaTab)
from interfazAnalisisNumerico import BiseccionTab, NewtonRaphsonTab, FalsaPosicionTab, SecanteTab
from interfazVectores import ProductoVectorTab, OperacionesVectorTab
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

class VectoresScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.cerrar_pestana)

        self.boton_panel = QWidget()
        self.boton_layout = QVBoxLayout(self.boton_panel)
        
        self.crear_boton("Operaciones con Vectores", OperacionesVectorTab)
        self.crear_boton("Producto de Vector Fila por Vector Columna", ProductoVectorTab)
        
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
    def __init__(self, cambiar_a_matrices, cambiar_a_analisis_numerico, cambiar_a_vectores):
        super().__init__()
        self.cambiar_a_matrices = cambiar_a_matrices
        self.cambiar_a_analisis_numerico = cambiar_a_analisis_numerico
        self.cambiar_a_vectores = cambiar_a_vectores

        # Layout principal horizontal
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        layout.setSpacing(0)  # Sin espacios entre layouts

        # ---------------------
        # Barra lateral
        # ---------------------
        barra_layout = QVBoxLayout()
        barra_layout.setSpacing(30)
        barra_layout.setContentsMargins(0, 50, 0, 0)  # Márgenes para empujar hacia abajo

        barra_widget = QWidget()
        barra_widget.setStyleSheet("""
            QWidget {
                background-color: #089bac;
                border-top-right-radius: 125px;
                border-bottom-right-radius: 125px;
            }
        """)
        barra_widget.setLayout(barra_layout)
        barra_widget.setFixedWidth(250)

        # Botones de la barra lateral
        boton_matrices = QPushButton()
        boton_matrices.setToolTip("Matrices")
        boton_matrices.setFixedSize(100, 100)
        boton_matrices.setIcon(QIcon(os.path.join("Assets", "matriz.png")))
        boton_matrices.setIconSize(boton_matrices.size())
        boton_matrices.clicked.connect(self.cambiar_a_matrices)
        barra_layout.addWidget(boton_matrices, alignment=Qt.AlignCenter)

        boton_vectores = QPushButton()
        boton_vectores.setToolTip("Vectores")
        boton_vectores.setFixedSize(100, 100)
        boton_vectores.setIcon(QIcon(os.path.join("Assets", "vector.png")))
        boton_vectores.setIconSize(boton_vectores.size())
        boton_vectores.clicked.connect(self.cambiar_a_vectores)
        barra_layout.addWidget(boton_vectores, alignment=Qt.AlignCenter)

        boton_analisis = QPushButton()
        boton_analisis.setToolTip("Análisis Numérico")
        boton_analisis.setFixedSize(100, 100)
        boton_analisis.setIcon(QIcon(os.path.join("Assets", "iconofx.png")))
        boton_analisis.setIconSize(boton_analisis.size())
        boton_analisis.clicked.connect(self.cambiar_a_analisis_numerico)
        barra_layout.addWidget(boton_analisis, alignment=Qt.AlignCenter)

        boton_ayuda = QPushButton()
        boton_ayuda.setToolTip("Ayuda(No implementado)")
        boton_ayuda.setFixedSize(100, 100)
        boton_ayuda.setIcon(QIcon(os.path.join("Assets", "ayuda.png")))
        boton_ayuda.setIconSize(boton_ayuda.size())
        boton_ayuda.clicked.connect(self.cambiar_a_analisis_numerico)
        barra_layout.addWidget(boton_ayuda, alignment=Qt.AlignCenter)

        boton_ajustes = QPushButton()
        boton_ajustes.setToolTip("Ajustes(No implementado)")
        boton_ajustes.setFixedSize(100, 100)
        boton_ajustes.setIcon(QIcon(os.path.join("Assets", "ajustes.png")))
        boton_ajustes.setIconSize(boton_ajustes.size())
        boton_ajustes.clicked.connect(self.cambiar_a_analisis_numerico)
        barra_layout.addWidget(boton_ajustes, alignment=Qt.AlignCenter)

        barra_layout.addStretch()
        layout.addWidget(barra_widget)
          # Agregar la barra lateral al layout principal

        # ---------------------
        # Sección central
        # ---------------------
        seccion_central_widget = QWidget()  # Contenedor para alinear correctamente
        seccion_central_layout = QVBoxLayout()
        seccion_central_layout.setContentsMargins(20, 20, 0, 20)  # Sin márgenes
        seccion_central_layout.setSpacing(20)  # Espacio entre elementos
        seccion_central_layout.setAlignment(Qt.AlignTop)  # Alineación hacia arriba

        # Logo
        ruta_logo = os.path.join("Assets", "logoSticker.png")
        logo = QLabel()
        pixmap = QPixmap(ruta_logo)
        logo.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Ajustar tamaño del logo
        logo.setAlignment(Qt.AlignCenter)
        seccion_central_layout.addWidget(logo, alignment=Qt.AlignCenter)

        # Descripción personalizada
        descripcion = QLabel(
            "¡Bienvenido a VisualCalc!\n\n"
            "VisualCalc es un sistema interactivo diseñado para trabajar con matrices, "
            "vectores y métodos de análisis numérico, ofreciendo explicaciones paso a paso.\n\n"
            "¿En qué quieres trabajar hoy?"
        )
        descripcion.setWordWrap(True)  # Ajuste de línea
        descripcion.setAlignment(Qt.AlignCenter)
        descripcion.setStyleSheet("font-size: 18px; color: #089bac; max-width: 600px;")
        seccion_central_layout.addWidget(descripcion, alignment=Qt.AlignCenter)

        # Botones principales
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(20)

        boton_matrices_central = QPushButton("Matrices")
        boton_matrices_central.setFixedSize(180, 50)
        boton_matrices_central.setStyleSheet("font-size: 16px; background-color: #089bac; color: white;")
        boton_matrices_central.clicked.connect(self.cambiar_a_matrices)
        botones_layout.addWidget(boton_matrices_central)

        boton_vectores_central = QPushButton("Vectores")
        boton_vectores_central.setFixedSize(180, 50)
        boton_vectores_central.setStyleSheet("font-size: 16px; background-color: #089bac; color: white;")
        boton_vectores_central.clicked.connect(self.cambiar_a_vectores)
        botones_layout.addWidget(boton_vectores_central)

        boton_analisis_central = QPushButton("Análisis Numérico")
        boton_analisis_central.setFixedSize(180, 50)
        boton_analisis_central.setStyleSheet("font-size: 16px; background-color: #089bac; color: white;")
        boton_analisis_central.clicked.connect(self.cambiar_a_analisis_numerico)
        botones_layout.addWidget(boton_analisis_central)

        # Agregar los botones al layout central
        seccion_central_layout.addLayout(botones_layout)

        # Establecer el layout para el contenedor central
        seccion_central_widget.setLayout(seccion_central_layout)

        # Agregar el contenedor central al layout principal con alineación explícita

        layout.addWidget(seccion_central_widget, alignment=Qt.AlignHCenter | Qt.AlignTop, stretch=1)

        # ---------------------
        # Imagen derecha
        # ---------------------
        ruta_elementos = os.path.join("Assets", "elementosderechacut.png")
        imagen_label = QLabel()
        pixmap = QPixmap(ruta_elementos)
        imagen_label.setPixmap(pixmap.scaledToWidth(250, Qt.SmoothTransformation))
        imagen_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(imagen_label, alignment=Qt.AlignRight)

        # Establecer layout principal
        self.setLayout(layout)

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
            cambiar_a_analisis_numerico=self.mostrar_analisis_numerico,
            cambiar_a_vectores=self.mostrar_vectores
        )
        self.stacked_widget.addWidget(self.menu_principal)

        self.matrices_screen = MatricesScreen()
        self.stacked_widget.addWidget(self.matrices_screen)

        self.vectores_screen = VectoresScreen()
        self.stacked_widget.addWidget(self.vectores_screen)

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

    def mostrar_vectores(self):

        self.stacked_widget.setCurrentWidget(self.vectores_screen)
        self.boton_volver.setVisible(True)
        self.dock_boton_panel.setWidget(self.vectores_screen.boton_panel)
        self.dock_boton_panel.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, "themes.qss")
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
