# interfaz.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QDialog, QGridLayout, QLabel, QLineEdit, QTextEdit, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from matrices import Matriz  # Importar la clase Matriz desde el archivo matrices.py


class IngresarMatrizDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Ingresar Matriz")

        # Layout principal vertical
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # Ajustar márgenes del layout
        self.main_layout.setSpacing(10)  # Espaciado entre los widgets
        
        self.init_ui()

    def init_ui(self):
        # Etiqueta y entrada para el número de ecuaciones
        top_layout = QVBoxLayout()
        
        self.n_label = QLabel("Número de ecuaciones:")
        self.n_input = QLineEdit()
    
        # Botón para ingresar la matriz
        self.ingresar_btn = QPushButton("Ingresar Matriz")
        self.ingresar_btn.clicked.connect(self.ingresar_matriz)


        # Layout horizontal para centrar el botón
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Añadir espacio flexible a la izquierda
        button_layout.addWidget(self.ingresar_btn)  # Añadir el botón
        button_layout.addStretch()  # Añadir espacio flexible a la derecha
        
        top_layout.addWidget(self.n_label)
        top_layout.addWidget(self.n_input)
        top_layout.addLayout(button_layout)
        
        self.main_layout.addLayout(top_layout)
        
        self.main_layout.addStretch()
                        
        self.grid_layout = None  # Variable para el grid layout que se añadirá después
        
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
                self.main_layout.removeItem(self.grid_layout)

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
            self.main_layout.addLayout(self.grid_layout)
            

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")

    def procesar_entradas(self, matriz):
        try:
            # Leer y validar las entradas de la matriz
            for i, fila_entradas in enumerate(self.entradas):
                for j, entrada in enumerate(fila_entradas):
                    valor_texto = entrada.text()
                    if valor_texto.strip() == "":
                        raise ValueError(f"El campo {i+1},{j+1} está vacío.")
                    valor = float(valor_texto)
                    matriz.matriz[i][j] = valor

            # Realizar la eliminación Gauss-Jordan y obtener los resultados
            resultado, pasos, soluciones = matriz.gauss_jordan_eliminacion()

            # Mostrar los resultados: matriz y soluciones
            self.mostrar_resultados(
                f"Soluciones:\n{soluciones}\n\nResultado:\n{matriz.mostrar()}\n\nPasos:\n{pasos}"
            )

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

    def mostrar_resultados(self, texto):
        # Método dedicado para mostrar los resultados y pasos, ajustable según tu preferencia
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        self.main_layout.addWidget(self.resultado_texto)
        
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
        
        titulo_layout = QHBoxLayout()
        titulo = QLabel("Calculadora de Matrices.\n\nSeleccione una opcion.")
        
        titulo_layout.addStretch()
        titulo_layout.addWidget(titulo)
        titulo_layout.addStretch()
        
        self.layout.addLayout(titulo_layout)
        self.layout.addStretch()
        # Botón para la eliminación Gauss-Jordan
        self.gauss_jordan_btn = QPushButton("Eliminación Gauss-Jordan")
        self.gauss_jordan_btn.clicked.connect(self.mostrar_ingresar_matriz_dialog)
        self.layout.addWidget(self.gauss_jordan_btn)
        self.layout.addStretch()

    def mostrar_ingresar_matriz_dialog(self):
        dialog = IngresarMatrizDialog()
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
