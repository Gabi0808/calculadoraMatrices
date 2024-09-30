import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matrices import Matriz, Vector
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys

class VisualizadorMatrizPorVector:
    def __init__(self, matriz, vector, resultado):
        self.matriz = matriz
        self.vector = vector 
        self.resultado = resultado

    def crear_grid_original(self, ax, rango_valores, paso):
        for x in range(-rango_valores, rango_valores + 1, paso):
            ax.plot([x, x], [-rango_valores, rango_valores], color='gray', linestyle='-', linewidth=1, alpha=0.3)

        for y in range(-rango_valores, rango_valores + 1, paso):
            ax.plot([-rango_valores, rango_valores], [y, y], color='gray', linestyle='-', linewidth=1, alpha=0.3)

        ax.set_aspect('equal')
        ax.grid(False)
        ax.set_xlim(-rango_valores, rango_valores)
        ax.set_ylim(-rango_valores, rango_valores)
    
    @staticmethod
    def dibujar_vector(ax, origen, vector, color):
        # Dibuja un vector en el gráfico dado un origen y un vector
        ax.arrow(origen[0], origen[1], vector[0], vector[1], 
                 head_width=0.2, head_length=0.3, fc=color, ec=color,alpha=0.7, 
                 linewidth=1,zorder=3)

    @staticmethod
    def interpolar_puntos(punto_inicial, punto_final, t):

        return [(1 - t) * punto_inicial[0] + t * punto_final[0], (1 - t) * punto_inicial[1] + t * punto_final[1]]

    def interpolar_grid(self, ax, rango_valores, paso, t):

        for x in range(-rango_valores, rango_valores + 1, paso):
            puntos_y = [[x, -rango_valores], [x, rango_valores]]
            puntos_y_transformados = [
                self.interpolar_puntos(p, self.matriz.multiplicar_matriz_por_vector(Vector(2, p))[0], t) for p in puntos_y
            ]
            ax.plot([p[0] for p in puntos_y_transformados], [p[1] for p in puntos_y_transformados], color='blue', linestyle='-', linewidth=1, alpha=0.5)

        for y in range(-rango_valores, rango_valores + 1, paso):
            puntos_x = [[-rango_valores, y], [rango_valores, y]]
            puntos_x_transformados = [
                self.interpolar_puntos(p, self.matriz.multiplicar_matriz_por_vector(Vector(2, p))[0], t) for p in puntos_x
            ]
            ax.plot([p[0] for p in puntos_x_transformados], [p[1] for p in puntos_x_transformados], color='blue', linestyle='-', linewidth=1, alpha=0.5)

    def interpolar_ejes(self, ax, rango_valores, t):

        eje_x_original = [-rango_valores, 0], [rango_valores, 0]
        eje_x_transformado = [
            self.matriz.multiplicar_matriz_por_vector(Vector(2, [-rango_valores, 0]))[0],
            self.matriz.multiplicar_matriz_por_vector(Vector(2, [rango_valores, 0]))[0]
        ]
        eje_y_original = [0, -rango_valores], [0, rango_valores]
        eje_y_transformado = [
            self.matriz.multiplicar_matriz_por_vector(Vector(2, [0, -rango_valores]))[0],
            self.matriz.multiplicar_matriz_por_vector(Vector(2, [0, rango_valores]))[0]
        ]

        eje_x = [self.interpolar_puntos(eje_x_original[0], eje_x_transformado[0], t), 
                 self.interpolar_puntos(eje_x_original[1], eje_x_transformado[1], t)]
        eje_y = [self.interpolar_puntos(eje_y_original[0], eje_y_transformado[0], t), 
                 self.interpolar_puntos(eje_y_original[1], eje_y_transformado[1], t)]

        ax.plot([eje_x[0][0], eje_x[1][0]], [eje_x[0][1], eje_x[1][1]], color='white', linewidth=1, linestyle='-', alpha=0.7)
        ax.plot([eje_y[0][0], eje_y[1][0]], [eje_y[0][1], eje_y[1][1]], color='white', linewidth=1, linestyle='-', alpha=0.7)

    def crear_vector_matriz(self, ax, t):

        colores = ['green', 'red']
        num_vectores = len(self.matriz.matriz[0])
        origen = (0, 0)

        for j in range(num_vectores):
            vector_original = [1 if i == j else 0 for i in range(num_vectores)]
            vector_transformado = self.matriz.multiplicar_matriz_por_vector(Vector(num_vectores, vector_original))[0]
            vector_interpolado = self.interpolar_puntos(vector_original, vector_transformado, t)
            self.dibujar_vector(ax, origen, vector_interpolado, colores[j])

    def dibujar_area_transformada(self, ax, t):

        origen = [0, 0]
        v1_original = [1, 0]
        v2_original = [0, 1]

        v1_transformado = self.matriz.multiplicar_matriz_por_vector(Vector(2, v1_original))[0]
        v2_transformado = self.matriz.multiplicar_matriz_por_vector(Vector(2, v2_original))[0]

        v1_interpolado = self.interpolar_puntos(v1_original, v1_transformado, t)
        v2_interpolado = self.interpolar_puntos(v2_original, v2_transformado, t)

        paralelogramo = Polygon([origen, v1_interpolado, [v1_interpolado[0] + v2_interpolado[0], v1_interpolado[1] + v2_interpolado[1]], v2_interpolado], color='yellow', alpha=0.5)
        ax.add_patch(paralelogramo)

    def visualizar_con_interpolacion(self, ax, rango_valores, paso, t):
        
        ax.clear()
        ax.set_facecolor('#101010')
        self.crear_grid_original(ax, rango_valores, paso)
        self.interpolar_grid(ax, rango_valores, paso, t)
        self.interpolar_ejes(ax, rango_valores, t)
        self.crear_vector_matriz(ax, t)
        self.dibujar_area_transformada(ax, t)
        ax.figure.canvas.draw()  # Redibuja el canvas


class SliderTransformacion(QWidget):
    def __init__(self, visualizador):
        super().__init__()
        
        self.visualizador = visualizador

        # Crear el layout vertical
        layout = QVBoxLayout()

        # Crear la figura y el canvas de matplotlib
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Crear el slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)  # Slider de 0 a 100 para representar t entre 0 y 1
        self.slider.setValue(0)  # Valor inicial del slider
        self.slider.setSingleStep(1)  # Incrementos de 0.01
        self.slider.valueChanged.connect(self.actualizar_transformacion)

        # Crear etiqueta para mostrar el valor de t
        self.label = QLabel(f't = 0.00')
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        # Asignar el layout
        self.setLayout(layout)

        # Visualización inicial con t = 0 (sin transformación)
        self.actualizar_transformacion()

    def actualizar_transformacion(self):
 
        t = self.slider.value() / 100.0  # t varía de 0 a 1 en pasos de 0.01
        self.label.setText(f't = {t:.2f}')
        self.visualizador.visualizar_con_interpolacion(self.ax, rango_valores=10, paso=1, t=t)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de Transformación con Slider")

        # Crear la matriz y el visualizador
        matriz = Matriz(2, 2)
        matriz.matriz = [[2, 1], [1, 3]]  # Matriz de ejemplo
        visualizador = VisualizadorMatrizPorVector(matriz, vector=None, resultado=None)

        # Crear el widget de SliderTransformacion
        self.slider_widget = SliderTransformacion(visualizador)
        self.setCentralWidget(self.slider_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())