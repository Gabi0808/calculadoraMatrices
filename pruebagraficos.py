import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class Grafico3D(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.ax = fig.add_subplot(111, projection='3d')
        super(Grafico3D, self).__init__(fig)

    def plot(self, matriz_transformacion):
        # Crear puntos en el espacio
        x = np.linspace(-1, 1, 10)
        y = np.linspace(-1, 1, 10)
        z = np.linspace(-1, 1, 10)

        # Crear una cuadrícula de puntos
        X, Y, Z = np.meshgrid(x, y, z)
        puntos = np.array([X.flatten(), Y.flatten(), Z.flatten()])

        # Aplicar transformación con la matriz dada
        puntos_transformados = np.dot(matriz_transformacion, puntos)

        # Limpiar el gráfico previo
        self.ax.clear()
        
        # Graficar puntos originales en rojo y transformados en azul
        self.ax.scatter(puntos[0], puntos[1], puntos[2], color='red', label='Original')
        self.ax.scatter(puntos_transformados[0], puntos_transformados[1], puntos_transformados[2], color='blue', label='Transformado')

        # Configurar los ejes y leyenda
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.legend()
        self.draw()

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Transformación de Espacio con Matrices')
        self.setGeometry(100, 100, 800, 600)

        # Crear widget central
        self.widget_central = QWidget()
        self.layout = QVBoxLayout()
        self.widget_central.setLayout(self.layout)
        self.setCentralWidget(self.widget_central)

        # Crear el gráfico 3D y añadirlo al layout
        self.grafico = Grafico3D(self)
        self.layout.addWidget(self.grafico)

        # Ejemplo de una matriz de transformación: rotación en 45 grados sobre el eje Z
        matriz_transformacion = np.array([
            [np.cos(np.pi/4), -np.sin(np.pi/4), 0],
            [np.sin(np.pi/4), np.cos(np.pi/4), 0],
            [0, 0, 1]
        ])

        # Graficar usando la matriz de transformación
        self.grafico.plot(matriz_transformacion)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
