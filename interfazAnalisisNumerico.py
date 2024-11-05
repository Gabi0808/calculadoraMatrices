from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QTabWidget, QMainWindow, QTextEdit)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sympy as sym
import sys
from matplotlib import pyplot as plt
from io import BytesIO
from analisisNumerico import Funcion

class BiseccionTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        # Layout para el menú de botones de símbolos matemáticos
        self.simbolos_layout = QHBoxLayout()
        self.agregar_botones_simbolos()

        # Campo de entrada para la función
        self.label_funcion = QLabel("Ingrese la función en términos de 'x':")
        self.input_funcion = QLineEdit()
        self.input_funcion.textChanged.connect(self.actualizar_latex)
        
        # Campo de entrada para el intervalo [a, b]
        self.contenedor_intervalos = QHBoxLayout()
        self.label_a = QLabel("Ingrese el valor de 'a':")
        self.input_a = QLineEdit()
        
        self.label_b = QLabel("Ingrese el valor de 'b':")
        self.input_b = QLineEdit()
        
        # Botón para ejecutar el método de bisección
        self.boton_calcular = QPushButton("Calcular Bisección")
        self.boton_calcular.clicked.connect(self.calcular_biseccion)
        
        # Label para mostrar la función en formato LaTeX
        self.latex_label = QLabel()
        self.latex_label.setAlignment(Qt.AlignCenter)
        
        # QTextEdit para mostrar el registro de iteraciones
        self.text_edit_resultado = QTextEdit()
        self.text_edit_resultado.setReadOnly(True)  # Solo lectura para el registro
        self.text_edit_resultado.setFontFamily("Courier New")  # Fuente monoespaciada

        # Agregar los widgets al layout
        self.main_layout.addWidget(self.latex_label)
        self.main_layout.addWidget(self.label_funcion)
        self.main_layout.addWidget(self.input_funcion)
        self.main_layout.addLayout(self.simbolos_layout) 
        
        self.contenedor_intervalos.addWidget(self.label_a)
        self.contenedor_intervalos.addWidget(self.input_a)
        self.contenedor_intervalos.addWidget(self.label_b)
        self.contenedor_intervalos.addWidget(self.input_b)
        self.main_layout.addLayout(self.contenedor_intervalos)
        self.main_layout.addWidget(self.boton_calcular)
        self.main_layout.addWidget(QLabel("Registro de iteraciones:"))
        self.main_layout.addWidget(self.text_edit_resultado)

    def agregar_botones_simbolos(self):
        # Crear botones para símbolos comunes y agregarlos al layout de símbolos
        simbolos = {
            "√": "sqrt(",    # Raíz cuadrada
            "sin": "sin(",   # Seno
            "cos": "cos(",   # Coseno
            "tan": "tan(",   # Tangente
            "ln": "ln(",     # Logaritmo natural
            "log": "log(",   # Logaritmo
            "^": "**",       # Exponente
            "/": "/",        # Fracción
            "π": "pi",       # Pi
            "e": "E"         # Número de Euler
        }
        
        for simbolo, expresion in simbolos.items():
            boton = QPushButton(simbolo)
            boton.clicked.connect(lambda _, exp=expresion: self.insertar_simbolo(exp))
            self.simbolos_layout.addWidget(boton)

    def insertar_simbolo(self, simbolo):
        # Insertar el símbolo en la posición actual del cursor en input_funcion
        cursor_pos = self.input_funcion.cursorPosition()
        texto_actual = self.input_funcion.text()
        nuevo_texto = texto_actual[:cursor_pos] + simbolo + texto_actual[cursor_pos:]
        
        # Actualizar el texto y establecer el foco en el campo de entrada
        self.input_funcion.setText(nuevo_texto)
        self.input_funcion.setFocus()  # Coloca el foco en el campo de entrada
        self.input_funcion.setCursorPosition(cursor_pos + len(simbolo))


    def actualizar_latex(self):
        # Obtener el texto de la función y convertirlo en una expresión de SymPy
        funcion_texto = self.input_funcion.text()
        try:
            funcion = Funcion(funcion_texto)
            latex_str = sym.latex(funcion.funcion)  # Convertir la función a LaTeX
            self.mostrar_latex(latex_str)
        except Exception:
            # Limpiar si hay un error de sintaxis en la entrada
            self.latex_label.clear()

    def mostrar_latex(self, latex_str):
        # Cambiar el tamaño de la figura según desees (ancho y alto en pulgadas)
        fig, ax = plt.subplots(figsize=(3, 0.5))  # Cambia el tamaño aquí

        # Renderizar el texto en formato LaTeX
        ax.text(0.5, 0.5, f"${latex_str}$", horizontalalignment='center', verticalalignment='center', fontsize=12)
        ax.axis('off')

        # Guardar la imagen en un buffer de memoria
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1)
        buffer.seek(0)
        plt.close(fig)

        # Mostrar la imagen en el QLabel sin guardarla en disco
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        self.latex_label.setPixmap(pixmap)

    def calcular_biseccion(self):
        try:
            funcion_texto = self.input_funcion.text()
            a = float(self.input_a.text())
            b = float(self.input_b.text())

            funcion = Funcion(funcion_texto)
            raiz, log = funcion.biseccion(a, b)  # Obtener la raíz y el registro de iteraciones
            
            # Mostrar el registro en el QTextEdit
            self.text_edit_resultado.setText(log)
            
            # Mostrar un mensaje con la raíz aproximada
            QMessageBox.information(self, "Resultado de Bisección", f"La raíz aproximada es: {raiz}")
        
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada no válida: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análisis Numérico")
        self.setGeometry(100, 100, 600, 400)
        
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        self.biseccion_tab = BiseccionTab()
        self.tab_widget.addTab(self.biseccion_tab, "Método de Bisección")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
