import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSpacerItem, QSizePolicy, QMessageBox, QTextEdit, QMainWindow, QWidget, QComboBox
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
class IngresarMatrizDialog(QDialog):
    def __init__(self, rectangular=False):
        super().__init__()
        self.rectangular = rectangular
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

        # Inputs para dimensiones de la matriz
        self.n_input = QLineEdit()
        self.m_input = QLineEdit()

        if self.rectangular:
            self.crear_layout_top(
                labels_inputs=[("Filas de la matriz:", self.n_input), ("Columnas de la matriz:", self.m_input)],
                boton_texto="Ingresar Matriz",
                boton_callback=self.ingresar_matriz
            )
        else:
            self.crear_layout_top(
                labels_inputs=[("Número de ecuaciones:", self.n_input)],
                boton_texto="Ingresar Matriz",
                boton_callback=self.ingresar_matriz
            )

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

    def ingresar_matriz(self):
        try:
            n = int(self.n_input.text())
            if n <= 0:
                raise ValueError("El número de filas debe ser un número entero positivo.")

            if self.rectangular:
                m = int(self.m_input.text())
                if m <= 0:
                    raise ValueError("El número de columnas debe ser un número entero positivo.")
            else:
                m = n + 1  # Para matrices cuadradas aumentadas

            self.matriz = Matriz(n, m)
            self.configurar_grid_layout(n, m, self.procesar_entradas)
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")

    def procesar_entradas(self):
        try:
            for i, fila_entradas in enumerate(self.entradas):
                for j, entrada in enumerate(fila_entradas):
                    valor_texto = entrada.text()
                    if valor_texto.strip() == "":
                        raise ValueError(f"El campo {i+1},{j+1} está vacío.")
                    valor = float(valor_texto)
                    self.matriz.matriz[i][j] = valor

            # Usar el método unificado eliminacion_gauss_jordan
            resultado, pasos, soluciones = self.matriz.eliminacion_gauss_jordan()
            self.mostrar_resultados(
                f"Soluciones:\n{soluciones}\n\nResultado:\n{self.matriz.mostrar()}\n\nPasos:\n{pasos}"
            )
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

    def mostrar_resultados(self, texto):
        if self.resultado_texto is not None:
            self.main_layout.removeWidget(self.resultado_texto)
        if self.placeholder_respuestas is not None:
            self.main_layout.removeWidget(self.placeholder_respuestas)
            self.placeholder_respuestas = None
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        self.resultado_texto.setFontFamily("Courier New")  # Fuente monoespaciada
        self.main_layout.addWidget(self.resultado_texto)
        self.resultado_texto.setText(texto)

class OperacionesVectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Vectores")
        self.setGeometry(100, 100, 500, 600)

        # Layout principal
        self.main_layout = QVBoxLayout()

        # Lista de vectores y escalares
        self.vector_inputs = []
        self.escalar_inputs = []

        # Área para los vectores y escalares
        self.inputs_layout = QVBoxLayout()
        self.main_layout.addLayout(self.inputs_layout)

        # Botón para agregar vectores
        agregar_btn = QPushButton("Agregar Vector")
        agregar_btn.clicked.connect(self.agregar_vector)
        self.main_layout.addWidget(agregar_btn)

        # Botón para eliminar el último vector
        eliminar_btn = QPushButton("Eliminar Último Vector")
        eliminar_btn.clicked.connect(self.eliminar_vector)
        self.main_layout.addWidget(eliminar_btn)

        # Botones para seleccionar la operación
        self.operacion_combo = QComboBox()
        self.operacion_combo.addItems(["Suma de vectores", "Combinación de vectores"])
        self.main_layout.addWidget(self.operacion_combo)

        # Botón para ejecutar la operación
        ejecutar_btn = QPushButton("Ejecutar Operación")
        ejecutar_btn.clicked.connect(self.ejecutar_operacion)
        self.main_layout.addWidget(ejecutar_btn)

        # Área de texto para mostrar resultados
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        self.resultado_texto.setFontFamily("Courier New")  # Fuente monoespaciada
        self.main_layout.addWidget(self.resultado_texto)

        self.setLayout(self.main_layout)

        # Agregar al menos dos campos al inicio
        self.agregar_vector()
        self.agregar_vector()

    def agregar_vector(self):
        layout = QHBoxLayout()

        escalar_input = QLineEdit()
        escalar_input.setPlaceholderText("Escalar (para combinación)")
        self.escalar_inputs.append(escalar_input)
        layout.addWidget(escalar_input)

        vector_input = QLineEdit()
        vector_input.setPlaceholderText("Vector (separado por comas)")
        self.vector_inputs.append(vector_input)
        layout.addWidget(vector_input)

        self.inputs_layout.addLayout(layout)

    def eliminar_vector(self):
        if self.vector_inputs:
            # Remover los campos de entrada
            vector_input = self.vector_inputs.pop()
            escalar_input = self.escalar_inputs.pop()
            vector_input.deleteLater()
            escalar_input.deleteLater()
            # Remover el layout
            layout = self.inputs_layout.takeAt(len(self.vector_inputs))
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                self.inputs_layout.removeItem(layout)

    def ejecutar_operacion(self):
        try:
            vectors = []
            escalars = []
            for idx, vector_input in enumerate(self.vector_inputs):
                vector_text = vector_input.text()
                if vector_text.strip() == "":
                    raise ValueError(f"El vector {idx + 1} está vacío.")
                vector = [float(x.strip()) for x in vector_text.split(",")]
                vectors.append(vector)

            operacion = self.operacion_combo.currentText()

            if operacion == "Suma de vectores":
                resultado, pasos = Matriz.sumar_vectores(*vectors)
                resultado_texto = pasos
                self.resultado_texto.setText(resultado_texto)

            elif operacion == "Combinación de vectores":
                for idx, escalar_input in enumerate(self.escalar_inputs):
                    escalar_text = escalar_input.text()
                    if escalar_text.strip() == "":
                        raise ValueError(f"El escalar {idx + 1} está vacío.")
                    escalar = float(escalar_text)
                    escalars.append(escalar)
                resultado, pasos = Matriz.combinar_vectores(escalars, vectors)
                resultado_texto = pasos
                self.resultado_texto.setText(resultado_texto)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))


class ProductoVectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Producto de Vector Fila por Vector Columna")
        self.setGeometry(100, 100, 500, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Input para el vector fila
        self.vector_fila_input = QLineEdit()
        layout.addWidget(QLabel("Vector Fila (separado por comas):"))
        layout.addWidget(self.vector_fila_input)

        # Input para el vector columna
        self.vector_columna_input = QLineEdit()
        layout.addWidget(QLabel("Vector Columna (separado por comas):"))
        layout.addWidget(self.vector_columna_input)

        # Botón para ejecutar la operación
        ejecutar_btn = QPushButton("Calcular Producto")
        ejecutar_btn.clicked.connect(self.calcular_producto)
        layout.addWidget(ejecutar_btn)

        # Área de texto para mostrar el resultado
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        self.resultado_texto.setFontFamily("Courier New")  # Fuente monoespaciada
        layout.addWidget(self.resultado_texto)

        self.setLayout(layout)

    def calcular_producto(self):
        try:
            vector_fila = [float(x.strip()) for x in self.vector_fila_input.text().split(",")]
            vector_columna = [float(x.strip()) for x in self.vector_columna_input.text().split(",")]
            resultado, pasos = Matriz.producto_vector_fila_por_vector_columna(vector_fila, vector_columna)
            resultado_texto = f"{pasos}\nResultado del producto: {resultado}"
            self.resultado_texto.setText(resultado_texto)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

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
        self.gauss_jordan_btn = QPushButton("Eliminación Gauss-Jordan (Matriz Cuadrada)")
        self.gauss_jordan_btn.clicked.connect(self.mostrar_ingresar_matriz_cuadrada_dialog)
        self.eliminacion_rectangular_btn = QPushButton("Eliminación Gauss-Jordan (Matriz Rectangular)")
        self.eliminacion_rectangular_btn.clicked.connect(self.mostrar_ingresar_matriz_rect_dialog)
        self.layout.addWidget(self.gauss_jordan_btn)
        self.layout.addWidget(self.eliminacion_rectangular_btn)
        self.operaciones_vector_btn = QPushButton("Operaciones con Vectores")
        self.operaciones_vector_btn.clicked.connect(self.mostrar_operaciones_vector_dialog)
        self.layout.addWidget(self.operaciones_vector_btn)
        self.producto_vector_btn = QPushButton("Producto de Vector Fila por Vector Columna")
        self.producto_vector_btn.clicked.connect(self.mostrar_producto_vector_dialog)
        self.layout.addWidget(self.producto_vector_btn)
        
        self.layout.addStretch()

    def mostrar_ingresar_matriz_cuadrada_dialog(self):
        dialog = IngresarMatrizDialog(rectangular=False)
        dialog.exec_()

    def mostrar_ingresar_matriz_rect_dialog(self):
        dialog = IngresarMatrizDialog(rectangular=True)
        dialog.exec_()

    def mostrar_operaciones_vector_dialog(self):
        dialog = OperacionesVectorDialog()
        dialog.exec_()
        
    def mostrar_producto_vector_dialog(self):
        dialog = ProductoVectorDialog()
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
