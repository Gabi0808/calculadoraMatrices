# interfaz.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QDialog, QGridLayout, QLabel, QLineEdit, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from matrices import Matriz  # Importar la clase Matriz desde el archivo matrices.py


class IngresarMatrizDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ingresar Matriz")
        self.layout = QVBoxLayout(self)  # Layout inicial del diálogo

        self.n_label = QLabel("Número de ecuaciones:")
        self.n_input = QLineEdit()
        self.layout.addWidget(self.n_label)
        self.layout.addWidget(self.n_input)

        self.ingresar_btn = QPushButton("Ingresar Matriz")
        self.ingresar_btn.clicked.connect(self.ingresar_matriz)
        self.layout.addWidget(self.ingresar_btn)

        self.grid_layout = None  # Variable para el grid layout que se añadirá después

        self.resultado_texto = None

    def ingresar_matriz(self):
        try:
            n = int(self.n_input.text())
            if n <= 0:
                raise ValueError("El número de ecuaciones debe ser un número entero positivo.")
            m = n + 1
            matriz = Matriz(n, m)

            # Verificar si ya existe un grid layout previo y eliminarlo
            if self.grid_layout is not None:
                # Eliminar el layout previo
                while self.grid_layout.count():
                    widget = self.grid_layout.takeAt(0).widget()
                    if widget is not None:
                        widget.deleteLater()
                self.layout.removeItem(self.grid_layout)

            # Crear un nuevo grid layout y agregarlo al layout principal
            self.grid_layout = QGridLayout()
            self.entradas = []

            for i in range(n):
                fila_entradas = []
                for j in range(m):
                    entrada = QLineEdit()
                    entrada.setPlaceholderText(f"Coef {i+1},{j+1}")

                    # Evitar que Enter borre el contenido al ser presionado
                    entrada.setClearButtonEnabled(False)
                    entrada.returnPressed.connect(lambda: None)  # Desconectar el Enter de la acción predeterminada

                    fila_entradas.append(entrada)
                    self.grid_layout.addWidget(entrada, i, j)
                self.entradas.append(fila_entradas)

            aceptar_btn = QPushButton("Aceptar")
            aceptar_btn.clicked.connect(lambda: self.procesar_entradas(matriz))
            self.grid_layout.addWidget(aceptar_btn, n, 0, 1, m)

            # Añadir el nuevo grid layout al layout principal
            self.layout.addLayout(self.grid_layout)

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")

    def procesar_entradas(self, matriz):
        try:
            for i, fila_entradas in enumerate(self.entradas):
                for j, entrada in enumerate(fila_entradas):
                    valor_texto = entrada.text()
                    # Validar que la entrada no esté vacía y sea un número válido
                    if valor_texto.strip() == "":
                        raise ValueError(f"El campo {i+1},{j+1} está vacío.")
                    valor = float(valor_texto)
                    matriz.matriz[i][j] = valor

            resultado, pasos = matriz.gauss_jordan_eliminacion()
            
            # Mover o modificar el setText donde quieras mostrar los resultados y pasos
            self.mostrar_resultados(f"Resultado:\n{matriz.mostrar()}\n\nPasos:\n{pasos}")

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

    def mostrar_resultados(self, texto):
        # Método dedicado para mostrar los resultados y pasos, ajustable según tu preferencia
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        self.layout.addWidget(self.resultado_texto)
        
        self.resultado_texto.setText(texto)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora de Matrices')
        self.setGeometry(100, 100, 400, 300)

        # Crear el widget central y el layout
        self.widget_central = QWidget()
        self.layout = QVBoxLayout()
        self.widget_central.setLayout(self.layout)
        self.setCentralWidget(self.widget_central)

        # Botón para la eliminación Gauss-Jordan
        self.gauss_jordan_btn = QPushButton("Eliminación Gauss-Jordan")
        self.gauss_jordan_btn.clicked.connect(self.mostrar_ingresar_matriz_dialog)
        self.layout.addWidget(self.gauss_jordan_btn)

    def mostrar_ingresar_matriz_dialog(self):
        dialog = IngresarMatrizDialog()
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
