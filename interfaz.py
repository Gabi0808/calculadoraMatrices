import sys
from PyQt5.QtWidgets import (QApplication,
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QSpacerItem, QSizePolicy, QMessageBox, QTextEdit, QMainWindow, QWidget
)
from PyQt5.QtCore import Qt
from matrices import Matriz

# Subclase personalizada de QLineEdit para manejar eventos de Enter correctamente
class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            event.accept()  # Ignorar el evento de Enter para que no cause efectos secundarios
        else:
            super().keyPressEvent(event)

# Clase base para los diálogos de ingreso de matrices
class BaseIngresarMatrizDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Ingresar Matriz")

        # Layout principal vertical
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        
        self.grid_layout = None
        self.entradas = []
        self.resultado_texto = None
        self.placeholder_respuestas = None

    def crear_layout_top(self, labels_inputs, boton_texto, boton_callback):

        top_layout = QVBoxLayout()
        inputs_layout = QHBoxLayout()

        for label_text, input_widget in labels_inputs:
            label = QLabel(label_text)
            inputs_layout.addWidget(label)
            inputs_layout.addWidget(input_widget)
        
        # Botón para ingresar la matriz
        ingresar_btn = QPushButton(boton_texto)
        ingresar_btn.clicked.connect(boton_callback)

        # Layout horizontal para centrar el botón
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ingresar_btn)
        button_layout.addStretch()

        top_layout.addLayout(inputs_layout)
        top_layout.addLayout(button_layout)
        self.main_layout.addLayout(top_layout)
        self.stretch_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(self.stretch_item)


    def configurar_grid_layout(self, n, m, aceptar_callback):
        # Verificar si ya existe un grid layout previo y eliminarlo
        if self.grid_layout is not None:
            while self.grid_layout.count():
                widget = self.grid_layout.takeAt(0).widget()
                if widget is not None:
                    widget.deleteLater()
            self.main_layout.removeItem(self.grid_layout)
        
        if self.stretch_item is not None:
            self.main_layout.removeItem(self.stretch_item)
            self.stretch_item = None

        # Crear un nuevo grid layout y agregarlo al layout principal
        self.grid_layout = QGridLayout()
        self.entradas = []

        for i in range(n):
            fila_entradas = []
            for j in range(m):
                entrada = CustomLineEdit()
                entrada.setPlaceholderText(f"Coef {i+1},{j+1}")
                fila_entradas.append(entrada)
                self.grid_layout.addWidget(entrada, i, j)
            self.entradas.append(fila_entradas)

        aceptar_btn = QPushButton("Aceptar")
        aceptar_btn.clicked.connect(aceptar_callback)
        self.grid_layout.addWidget(aceptar_btn, n, 0, 1, m)
        self.main_layout.addLayout(self.grid_layout)

        if self.placeholder_respuestas is None:
            self.placeholder_respuestas = QTextEdit()
            self.placeholder_respuestas.setReadOnly(True)
            self.main_layout.addWidget(self.placeholder_respuestas)

    def mostrar_resultados(self, texto):
        if self.resultado_texto is not None:
            self.main_layout.removeWidget(self.resultado_texto)
        self.main_layout.removeWidget(self.placeholder_respuestas)
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        self.main_layout.addWidget(self.resultado_texto)
        self.resultado_texto.setText(texto)

# Clase derivada específica para la eliminación Gauss-Jordan de matrices cuadradas
class IngresarMatrizDialog(BaseIngresarMatrizDialog):
    def __init__(self):
        super().__init__()
        self.n_input = QLineEdit()
        self.crear_layout_top(
            labels_inputs=[("Número de ecuaciones:", self.n_input)], 
            boton_texto="Ingresar Matriz", 
            boton_callback=self.ingresar_matriz
        )

    def ingresar_matriz(self):
        try:
            n = int(self.n_input.text())
            if n <= 0:
                raise ValueError("El número de ecuaciones debe ser un número entero positivo.")
            m = n + 1
            matriz = Matriz(n, m)
            self.configurar_grid_layout(n, m, lambda: self.procesar_entradas(matriz))
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")

    def procesar_entradas(self, matriz):
        try:
            for i, fila_entradas in enumerate(self.entradas):
                for j, entrada in enumerate(fila_entradas):
                    valor_texto = entrada.text()
                    if valor_texto.strip() == "":
                        raise ValueError(f"El campo {i+1},{j+1} está vacío.")
                    valor = float(valor_texto)
                    matriz.matriz[i][j] = valor

            resultado, pasos, soluciones = matriz.gauss_jordan_eliminacion()
            self.mostrar_resultados(
                f"Soluciones:\n{soluciones}\n\nResultado:\n{matriz.mostrar()}\n\nPasos:\n{pasos}"
            )
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

# Clase derivada específica para la eliminación de matrices rectangulares
class IngresarMatrizRectDialog(BaseIngresarMatrizDialog):
    def __init__(self):
        super().__init__()
        self.n_input = QLineEdit()
        self.m_input = QLineEdit()
        self.crear_layout_top(
            labels_inputs=[("Filas de la matriz:", self.n_input), ("Columnas de la matriz:", self.m_input)], 
            boton_texto="Ingresar Matriz", 
            boton_callback=self.ingresar_matriz_rect
        )

    def ingresar_matriz_rect(self):
        try:
            n = int(self.n_input.text())
            if n <= 0:
                raise ValueError("El número de filas debe ser un número entero positivo.")
            m = int(self.m_input.text())
            if m <= 0:
                raise ValueError("El número de columnas debe ser un número entero positivo.")
            matriz = Matriz(n, m)
            self.configurar_grid_layout(n, m, lambda: self.procesar_entradas_rect(matriz))
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")

    def procesar_entradas_rect(self, matriz):
        try:
            for i, fila_entradas in enumerate(self.entradas):
                for j, entrada in enumerate(fila_entradas):
                    valor_texto = entrada.text()
                    if valor_texto.strip() == "":
                        raise ValueError(f"El campo {i+1},{j+1} está vacío.")
                    valor = float(valor_texto)
                    matriz.matriz[i][j] = valor

            resultado, pasos, soluciones = matriz.eliminacion_rectangular()
            self.mostrar_resultados(
                f"Soluciones:\n{soluciones}\n\nResultado:\n{matriz.mostrar()}\n\nPasos:\n{pasos}"
            )
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

# Clase principal de la aplicación
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora de Matrices')
        self.setGeometry(100, 100, 400, 300)
        self.widget_central = QWidget()
        self.layout = QVBoxLayout()
        self.widget_central.setLayout(self.layout)
        self.setCentralWidget(self.widget_central)
        
        titulo_layout = QHBoxLayout()
        titulo = QLabel("Calculadora de Matrices.\n\nSeleccione una opción.")
        
        titulo_layout.addStretch()
        titulo_layout.addWidget(titulo)
        titulo_layout.addStretch()
        
        self.layout.addLayout(titulo_layout)
        self.layout.addStretch()

        # Botones para los diferentes métodos de eliminación
        self.gauss_jordan_btn = QPushButton("Eliminación Gauss-Jordan")
        self.gauss_jordan_btn.clicked.connect(self.mostrar_ingresar_matriz_dialog)
        self.eliminacion_rectangular_btn = QPushButton("Eliminación de matrices rectangulares\nde forma escalonada")
        self.eliminacion_rectangular_btn.clicked.connect(self.mostrar_ingresar_matriz_rect_dialog)
        self.layout.addWidget(self.gauss_jordan_btn)
        self.layout.addWidget(self.eliminacion_rectangular_btn)
        self.layout.addStretch()

    def mostrar_ingresar_matriz_dialog(self):
        dialog = IngresarMatrizDialog()
        dialog.exec_()
    
    def mostrar_ingresar_matriz_rect_dialog(self):
        dialog = IngresarMatrizRectDialog()
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
