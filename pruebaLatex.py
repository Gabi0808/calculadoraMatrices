import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from sympy import symbols, sympify, latex

class FunctionEvaluator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Crear el diseño de la interfaz
        layout = QVBoxLayout()

        # Campo de entrada para la función en formato LaTeX
        self.label_func = QLabel("Ingresa la función en términos de 'x':")
        layout.addWidget(self.label_func)
        
        self.input_func = QLineEdit(self)
        self.input_func.textChanged.connect(self.update_latex_preview)  # Conectar para vista previa en LaTeX
        layout.addWidget(self.input_func)

        # Campo de entrada para el valor de x
        self.label_x = QLabel("Ingresa el valor de x para evaluar:")
        layout.addWidget(self.label_x)
        
        self.input_x = QLineEdit(self)
        layout.addWidget(self.input_x)

        # Botón para evaluar la función
        self.button = QPushButton("Evaluar función", self)
        self.button.clicked.connect(self.evaluate_function)
        layout.addWidget(self.button)

        # Etiqueta para mostrar la función en formato LaTeX
        self.latex_label = QLabel(self)
        self.latex_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.latex_label)

        # Configurar la ventana principal
        self.setLayout(layout)
        self.setWindowTitle("Evaluador de Funciones con LaTeX en Tiempo Real")
        self.setGeometry(100, 100, 400, 300)

    def update_latex_preview(self):
        # Actualizar la vista previa de LaTeX mientras se escribe
        func_text = self.input_func.text()
        try:
            # Convertir a LaTeX usando sympy
            func_expr = sympify(func_text)
            func_latex = latex(func_expr)
            self.display_latex(func_latex)
        except:
            # En caso de error, no se muestra nada (el usuario puede estar escribiendo)
            self.latex_label.clear()

    def evaluate_function(self):
        # Capturar el texto de entrada de la función y el valor de x
        func_text = self.input_func.text()
        x_value_text = self.input_x.text()

        try:
            # Definir el símbolo
            x = symbols('x')

            # Convertir la función de texto a una expresión de SymPy
            func_expr = sympify(func_text)

            # Generar la representación en LaTeX y mostrarla
            func_latex = latex(func_expr)
            self.display_latex(func_latex)

            # Evaluar la función en el valor de x proporcionado
            x_value = float(x_value_text)
            result = func_expr.subs(x, x_value).evalf()

            # Mostrar el resultado en la etiqueta LaTeX
            self.display_latex(f"{func_latex} \\text{{ evaluado en }} x = {x_value} \\text{{ es }} {result}")

        except Exception as e:
            # Mostrar mensaje de error en caso de un problema con la entrada
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def display_latex(self, latex_str):
        # Crear una figura para renderizar el LaTeX con Matplotlib
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"${latex_str}$", horizontalalignment='center', verticalalignment='center', fontsize=12)
        ax.axis('off')

        # Guardar la imagen como un archivo temporal y cargarla en QLabel
        fig.savefig("latex_preview.png", bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)

        # Mostrar la imagen en el QLabel
        pixmap = QPixmap("latex_preview.png")
        self.latex_label.setPixmap(pixmap)

# Crear la aplicación y la ventana principal
app = QApplication(sys.argv)
window = FunctionEvaluator()
window.show()
sys.exit(app.exec_())
