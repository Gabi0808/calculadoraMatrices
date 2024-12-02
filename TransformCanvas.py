import sys
from PyQt5.QtWidgets import QTextEdit, QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from CustomPlotCanvas import CustomPlotCanvas

from matrices import Matriz, Vector
from transformacion import Transformacion, Visualizador


from PyQt5.QtWidgets import QVBoxLayout, QSlider, QLabel, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class TransformCanvas(CustomPlotCanvas):
    def __init__(self, matriz, vector, parent=None):
        super().__init__(parent)

        # Inicializar la lógica de transformación
        self.matriz = matriz
        self.vector = vector
        self.transformacion = Transformacion(self.matriz, self.vector)
        self.visualizador = Visualizador(self.transformacion)

        # Variable para la interpolación
        self.t = 0

        # Crear el layout principal que incluirá el canvas, slider y barra de navegación
        self.layout = QVBoxLayout()

        # Añadir el canvas al layout
        self.layout.addWidget(self)

        self.datos = QTextEdit()
        self.datos.setMaximumHeight(150)
        self.datos.setReadOnly(True)
        self.layout.addWidget(self.datos)

        # Añadir el slider con su etiqueta
        self.slider_label = QLabel("Interpolar (t): 0.0")
        self.slider_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(0)  # Valor inicial de t = 0
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.on_slider_change)  # Conectar evento
        self.layout.addWidget(self.slider)

        self.update_visualizacion()

        # Widget principal para contener el layout
        self.container = QWidget()
        self.container.setLayout(self.layout)

    def get_widget(self):
        """Devuelve el widget contenedor para añadirlo a una ventana."""
        return self.container

    def set_interpolacion(self, t):
        """Establecer el valor de interpolación y actualizar la visualización."""
        self.t = t
        self.update_visualizacion()

    def update_visualizacion(self):
        """Actualizar la visualización según el valor de t."""
        self.visualizador.borrar_elementos_dinamicos()
        self.visualizador.crear_grid(self.ax, self.t)
        self.visualizador.visualizar(self.ax, self.t)

    def on_slider_change(self, value):
        """Actualizar el valor de interpolación en el canvas."""
        t = value / 100  # Normalizar el valor del slider entre 0 y 1
        self.slider_label.setText(f"Interpolate (t): {t:.2f}")
        self.set_interpolacion(t)

    def wheelEvent(self, event):
        """Sobreescribir el evento de la rueda del mouse para incluir redibujado."""
        super().wheelEvent(event)
        self.update_visualizacion()

