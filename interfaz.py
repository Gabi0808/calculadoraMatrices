import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSpacerItem, QSizePolicy, QMessageBox, QTextEdit, QMainWindow, QWidget, QComboBox,QSlider, QCheckBox, QLayout
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matrices import Matriz
from vectores import Vector
from utilidades import *
from visualizador import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            event.accept()  
        else:
            super().keyPressEvent(event)
            
class InterfazHelper():
    def __init__(self):
        pass

    @staticmethod    
    def crear_layout_ingresar_dimensiones(labels_inputs, boton_texto, boton_callback):
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
        
        return top_layout
     
    @staticmethod 
    def limpiar_grid_layout(grid_layout, target_layout):
         if grid_layout is not None:
            while grid_layout.count():
                widget = grid_layout.takeAt(0).widget()
                if widget is not None:
                    widget.deleteLater()
            target_layout.removeItem(grid_layout)

    @staticmethod
    def configurar_grid_layout(n, m, aceptar_callback, nombre_boton="Aceptar",inlcuir_boton=True):
        grid_layout = QGridLayout()
        entradas = []

        for i in range(n):
            fila_entradas = []
            for j in range(m):
                entrada = CustomLineEdit()
                entrada.setPlaceholderText(f"Coef {i+1},{j+1}")
                fila_entradas.append(entrada)
                grid_layout.addWidget(entrada, i, j)
            entradas.append(fila_entradas)
        
        if inlcuir_boton:
            aceptar_btn = QPushButton(nombre_boton)
            aceptar_btn.clicked.connect(aceptar_callback)
            grid_layout.addWidget(aceptar_btn, n, 0, 1, m)            
        
        return grid_layout, entradas

    @staticmethod
    def leer_entradas_dimensiones_matrices(n_input, m_input, rectangular):
        try:
            n = int(n_input.text())
            if n <= 0:
                raise ValueError("El número de filas debe ser un número entero positivo.")

            if rectangular:
                m = int(m_input.text())
                if m <= 0:
                    raise ValueError("El número de columnas debe ser un número entero positivo.")
            else:
                m = n + 1  # Para matrices cuadradas aumentadas
            return n, m
            
        except ValueError as e:
            QMessageBox.critical("Error", f"Entrada inválida: {str(e)}")
    
    @staticmethod
    def procesar_entradas_matrices(entradas):
        
        matriz_valores = [[] for _ in range(len(entradas))]

        try:
            for i, fila_entradas in enumerate(entradas):
                for j, entrada in enumerate(fila_entradas):
                    valor_texto = entrada.text()
                    if valor_texto.strip() == "":
                        raise ValueError(f"El campo {i+1},{j+1} está vacío.")
                    valor = float(valor_texto)
                    matriz_valores[i].append(valor)
        
            return matriz_valores
                    
        except ValueError as e:
            QMessageBox.critical(None, "Error", f"Error al ingresar datos: {str(e)}")
            raise
    
    @staticmethod
    def ingresar_matriz(instancia, main_layout, resultado_texto, grid_layout, n_input, m_input, calcular_callback, nombre_boton, target_layout, rectangular=True):
        try:
            InterfazHelper.limpiar_resultados_texto(resultado_texto, main_layout)
            InterfazHelper.limpiar_grid_layout(grid_layout, target_layout)

            # Leer dimensiones
            n, m = InterfazHelper.leer_entradas_dimensiones_matrices(n_input, m_input, rectangular=rectangular)

            nueva_matriz = Matriz(n, m)

            # Configurar nuevo grid_layout y asignarlo a la referencia actual
            nuevo_grid_layout, nuevas_entradas = InterfazHelper.configurar_grid_layout(n, m, calcular_callback, nombre_boton=nombre_boton)
            
            instancia.matriz = nueva_matriz
            instancia.grid_layout = nuevo_grid_layout
            instancia.entradas = nuevas_entradas
            target_layout.addLayout(instancia.grid_layout)
        
        except ValueError as e:
            QMessageBox.critical(None, "Error", f"Entrada inválida: {str(e)}")
            return None, None, None

    @staticmethod
    def ingresar_multiples_matrices(instancia, main_layout, resultado_texto, grid_layouts, n_inputs, m_inputs, nombre_boton, operacion_callback, target_layout, rectangular=True):
        try:
            InterfazHelper.limpiar_resultados_texto(resultado_texto, main_layout)

            for item in grid_layouts:
                if isinstance(item, QLayout):
                    InterfazHelper.limpiar_grid_layout(item, target_layout)
                elif isinstance(item, QWidget):
                    target_layout.removeWidget(item)
                    item.deleteLater()

            grid_layouts.clear()

            if hasattr(instancia, "boton_operacion") and instancia.boton_operacion is not None:
                target_layout.removeWidget(instancia.boton_operacion)
                instancia.boton_operacion.deleteLater()
                instancia.boton_operacion = None

            layout_matrices = QHBoxLayout()
            nuevas_matrices = []
            nuevas_entradas = []

            for i in range(len(n_inputs)):
                n, m = InterfazHelper.leer_entradas_dimensiones_matrices(n_inputs[i], m_inputs[i], rectangular=rectangular)
                nueva_matriz = Matriz(n, m)
                nuevas_matrices.append(nueva_matriz)

                nuevo_grid_layout, entradas = InterfazHelper.configurar_grid_layout(n, m, aceptar_callback=None, nombre_boton=None, inlcuir_boton=False)
                grid_layouts.append(nuevo_grid_layout)
                nuevas_entradas.append(entradas)

                matriz_layout = QVBoxLayout()
                etiqueta = QLabel(f"Matriz {i + 1}")
                etiqueta.setAlignment(Qt.AlignCenter)
                matriz_layout.addWidget(etiqueta)
                matriz_layout.addLayout(nuevo_grid_layout)
                layout_matrices.addLayout(matriz_layout)

                # Almacenar la etiqueta en grid_layouts para poder eliminarla posteriormente
                grid_layouts.append(etiqueta)

                if i < len(n_inputs) - 1:
                    layout_matrices.addSpacing(20)

            layout_con_matrices_y_boton = QVBoxLayout()
            layout_con_matrices_y_boton.addLayout(layout_matrices)

            # Crear y agregar el botón de operación
            instancia.boton_operacion = QPushButton(nombre_boton)
            instancia.boton_operacion.clicked.connect(operacion_callback)
            layout_con_matrices_y_boton.addWidget(instancia.boton_operacion)

            target_layout.addLayout(layout_con_matrices_y_boton)

            instancia.matrices = nuevas_matrices
            instancia.entradas_matrices = nuevas_entradas

        except ValueError as e:
            QMessageBox.critical(None, "Error", f"Entrada inválida: {str(e)}")
            return None, None, None

    @staticmethod
    def mostrar_resultados(texto):
        
        resultado_texto = QTextEdit()
        resultado_texto.setReadOnly(True)
        resultado_texto.setFontFamily("Courier New")  # Fuente monoespaciada
        resultado_texto.setText(texto)
        
        return resultado_texto
    
    @staticmethod
    def limpiar_resultados_texto(resultado_texto, main_layout):
        if resultado_texto is not None:
            main_layout.removeWidget(resultado_texto)
    
    @staticmethod
    def crear_layout_vectores(n_input, ingresar_dimension_callback):
        contenedor_layout = QVBoxLayout()
        contenedor_botones_layout = QVBoxLayout()
        contenedor_vectores_layout = QHBoxLayout()
        
        dimension_layout = InterfazHelper.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Dimensión de los vectores:", n_input)],
            boton_texto="Ingresar dimensión",
            boton_callback=ingresar_dimension_callback 
        )

        contenedor_vectores_layout.addLayout(dimension_layout)
        contenedor_layout.addLayout(contenedor_vectores_layout)
        contenedor_layout.addLayout(contenedor_botones_layout)

        return contenedor_layout, contenedor_vectores_layout, contenedor_botones_layout

    @staticmethod
    def limpiar_botones_vectores(contenedor_layout):
        while contenedor_layout.count():
            item = contenedor_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    @staticmethod
    def crear_botones_vectores(agregar_vector_callback, eliminar_vector_callback, ejecutar_operacion_callback, contenedor_layout):
        
        InterfazHelper.limpiar_botones_vectores(contenedor_layout)

        agregar_btn = QPushButton("Agregar Vector")
        agregar_btn.clicked.connect(agregar_vector_callback)
        contenedor_layout.addWidget(agregar_btn)
        
        eliminar_btn = QPushButton("Eliminar Último Vector")
        eliminar_btn.clicked.connect(eliminar_vector_callback)
        contenedor_layout.addWidget(eliminar_btn)
        
        ejecutar_btn = QPushButton("Calcular")
        ejecutar_btn.clicked.connect(ejecutar_operacion_callback)
        contenedor_layout.addWidget(ejecutar_btn)
        
    @staticmethod
    def leer_entrada_dimension_vector(n_input):
        try:
            n = int(n_input.text())
            if n <= 0:
                raise ValueError("El número de filas debe ser un número entero positivo.")
            
            return n
        
        except ValueError as e:
            QMessageBox.critical(None,"Error", f"Entrada inválida: {str(e)}")
            raise
        
    @staticmethod
    def crear_entrada_vector(dimension, orientacion="vertical"):
        contenedor_vectores_inputs = QVBoxLayout()

        # Layout para el escalar
        escalar_input_layout = QHBoxLayout()
        label = QLabel("Escalar del vector:")
        escalar_line_edit = QLineEdit()
        escalar_input_layout.addWidget(label)
        escalar_input_layout.addWidget(escalar_line_edit)
        entrada_escalar = [(label, escalar_line_edit)]

        # Layout para los componentes del vector
        grid_layout = QGridLayout()
        entradas_vector = []

        for i in range(dimension):
            etiqueta = QLabel(f"Componente {i + 1}:")
            entrada = QLineEdit()
            entrada.setPlaceholderText(f"Valor {i + 1}")

            if orientacion == "vertical":
                # Colocar la etiqueta y el campo de entrada en filas separadas
                grid_layout.addWidget(etiqueta, i, 0)
                grid_layout.addWidget(entrada, i, 1)
            elif orientacion == "horizontal":
                # Colocar la etiqueta arriba del campo de entrada
                v_layout = QVBoxLayout()
                v_layout.addWidget(etiqueta)
                v_layout.addWidget(entrada)
                grid_layout.addLayout(v_layout, 0, i)  # Añadir el VBoxLayout en una sola fila
            else:
                raise ValueError("La orientación debe ser 'vertical' u 'horizontal'")

            entradas_vector.append((etiqueta, entrada))

        contenedor_vectores_inputs.addLayout(escalar_input_layout)
        contenedor_vectores_inputs.addLayout(grid_layout)
        
        return entrada_escalar, entradas_vector, contenedor_vectores_inputs

    
    @staticmethod
    def agregar_campo_vector(vector_inputs, escalar_inputs, layout, n, orientacion="vertical"):
        
        entrada_escalar, entrada_vector, contenedor_entradas_vector = InterfazHelper.crear_entrada_vector(n, orientacion)
        
        layout.addLayout(contenedor_entradas_vector)
        
        vector_inputs.append(entrada_vector)
        escalar_inputs.append(entrada_escalar)
    
    @staticmethod    
    def eliminar_vector(vector_inputs, entrada_escalar, inputs_layout):
        if vector_inputs:
            
            entradas_vector = vector_inputs.pop()
            entrada_escalar = entrada_escalar.pop()

            for etiqueta, entrada in entrada_escalar:
                etiqueta.deleteLater()
                entrada.deleteLater()
            
            for etiqueta, entrada in entradas_vector:
                etiqueta.deleteLater()
                entrada.deleteLater()

            item_layout = inputs_layout.takeAt(inputs_layout.count() - 1)
            if isinstance(item_layout, QLayout):
                while item_layout.count():
                    item = item_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                item_layout.deleteLater()
            elif item_layout:
                widget = item_layout.widget()
                if widget:
                    widget.deleteLater()
            inputs_layout.removeItem(item_layout)

    @staticmethod
    def limpiar_entradas_vectores(vector_inputs, escalar_inputs, inputs_layout):
        while vector_inputs:
            InterfazHelper.eliminar_vector(vector_inputs, escalar_inputs, inputs_layout) 

    @staticmethod
    def procesar_entrada(entradas_vector, entradas_escalar, orientacion="vertical"):
        vectores = []
        escalares = []

        for idx, vector_input in enumerate(entradas_vector):
            valores_vector = []
            for _, entrada in vector_input:
                vector_text = entrada.text()
                if vector_text.strip() == "":
                    raise ValueError(f"El vector {idx + 1} tiene componentes vacíos.")
                valores_vector.append(float(vector_text))
            vectores.append(Vector(len(valores_vector), valores_vector, orientacion))

        for idx, escalar_input in enumerate(entradas_escalar):
            escalar_text = escalar_input.text()
            if escalar_text.strip() == "":
                raise ValueError(f"El escalar para el vector {idx + 1} está vacío.")
            escalares.append(float(escalar_text))

        if len(vectores) != len(escalares):
            raise ValueError("El número de vectores y escalares no coincide.")

        for i, vector in enumerate(vectores):
            vectores[i] = vector.escalar_vector(escalares[i])

        return vectores
    
    @staticmethod
    def configurar_matriz_y_vector(instancia, main_layout, resultado_texto, grid_layout, n_input, calcular_callback, nombre_boton, target_layout):
        try:
            
            n = int(n_input.text())
            if n <= 0:
                raise ValueError("El número de ecuaciones debe ser un número entero positivo.")

            InterfazHelper.limpiar_resultados_texto(resultado_texto, main_layout)
            InterfazHelper.limpiar_grid_layout(grid_layout, target_layout)

            layout_matriz_vector = QHBoxLayout()

            layout_matriz = QVBoxLayout()
            etiqueta_matriz = QLabel("Matriz")
            etiqueta_matriz.setAlignment(Qt.AlignCenter)
            layout_matriz.addWidget(etiqueta_matriz)

            grid_layout_matriz, entradas_matriz = InterfazHelper.configurar_grid_layout(n, n, aceptar_callback=None, nombre_boton=None, inlcuir_boton=False)
            layout_matriz.addLayout(grid_layout_matriz)

            layout_vector = QVBoxLayout()
            etiqueta_vector = QLabel("Vector de Constantes")
            etiqueta_vector.setAlignment(Qt.AlignCenter)
            layout_vector.addWidget(etiqueta_vector)

            entradas_vector = []
            for i in range(n):
                entrada = QLineEdit()
                entrada.setPlaceholderText(f"Constante {i + 1}")
                layout_vector.addWidget(entrada)
                entradas_vector.append(entrada)

            layout_matriz_vector.addLayout(layout_matriz)
            layout_matriz_vector.addSpacing(20)
            layout_matriz_vector.addLayout(layout_vector)

            target_layout.addLayout(layout_matriz_vector)

            if hasattr(instancia, "boton_operacion") and instancia.boton_operacion is not None:
                target_layout.removeWidget(instancia.boton_operacion)
                instancia.boton_operacion.deleteLater()
                instancia.boton_operacion = None

            instancia.boton_operacion = QPushButton(nombre_boton)
            instancia.boton_operacion.clicked.connect(calcular_callback)
            target_layout.addWidget(instancia.boton_operacion)

            instancia.entradas_matriz = entradas_matriz
            instancia.entradas_vector = entradas_vector
            instancia.layout_grid = layout_matriz_vector

        except ValueError as e:
            QMessageBox.critical(None, "Error", str(e))

    @staticmethod
    def ingresar_vectores(dimension_input, vector_inputs, escalar_inputs, contenedor_vectores_layout, contenedor_botones_layout, ejecutar_callback, orientaciones=["vertical", "vertical"]):
  
        n = InterfazHelper.leer_entrada_dimension_vector(dimension_input)

        if n is None:
            return

        InterfazHelper.crear_botones_vectores(
            lambda: InterfazHelper.agregar_campo_vector(vector_inputs, escalar_inputs, contenedor_vectores_layout, n, orientaciones[len(vector_inputs) % len(orientaciones)]),
            lambda: InterfazHelper.eliminar_vector(vector_inputs, escalar_inputs, contenedor_vectores_layout),
            ejecutar_callback,
            contenedor_botones_layout
        )

        InterfazHelper.limpiar_entradas_vectores(vector_inputs, escalar_inputs, contenedor_vectores_layout)

        for orientacion in orientaciones:
            InterfazHelper.agregar_campo_vector(vector_inputs, escalar_inputs, contenedor_vectores_layout, n, orientacion)

    @staticmethod
    def leer_entrada_vectores_escalares(vector_inputs, escalar_inputs):
        try:

            valores_vector = [elemento for elemento in vector_inputs]
            valores_escalar = [entrada[0][1] for entrada in escalar_inputs]

            lista_vectores_escalados = InterfazHelper.procesar_entrada(valores_vector, valores_escalar)

            return lista_vectores_escalados

        except ValueError as e:
            QMessageBox.critical(None, "Error al procesar entradas", str(e))
            return []

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
        self.main_layout.setAlignment(Qt.AlignTop)
        
        self.entradas = []
        self.grid_layout=None
        self.resultado_texto = None
        self.placeholder_respuestas = None
        self.matriz:Matriz = None
        
        # Inputs para dimensiones de la matriz
        self.n_input = QLineEdit()
        self.m_input = QLineEdit()
         
        if self.rectangular:
            
            layout_dimensiones_matriz = InterfazHelper.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Filas de la matriz:", self.n_input), ("Columnas de la matriz: ", self.m_input)],
            boton_texto="Ingresar Matriz",
            boton_callback=lambda: InterfazHelper.ingresar_matriz(instancia=self,
                                                                  main_layout=self.main_layout,
                                                                  resultado_texto=self.resultado_texto,
                                                                  grid_layout=self.grid_layout, 
                                                                  n_input=self.n_input, 
                                                                  m_input=self.m_input,
                                                                  calcular_callback=self.resolver_gauss, 
                                                                  nombre_boton="Resolver Matriz por Gauss-Jordan",
                                                                  target_layout=self.main_layout,
                                                                  rectangular=True
                                                                )
         
                )
        else:
            layout_dimensiones_matriz = InterfazHelper.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Dimensiones de la matriz:", self.n_input)],
            boton_texto="Ingresar Matriz",
            boton_callback=lambda: InterfazHelper.ingresar_matriz(instancia=self,
                                                                  main_layout=self.main_layout,
                                                                  resultado_texto=self.resultado_texto,
                                                                  grid_layout=self.grid_layout, 
                                                                  n_input=self.n_input, 
                                                                  m_input=self.m_input,
                                                                  calcular_callback=self.resolver_gauss, 
                                                                  nombre_boton="Resolver Matriz por Gauss-Jordan",
                                                                  target_layout=self.main_layout,
                                                                  rectangular=False
                                                                )
         )


        self.main_layout.addLayout(layout_dimensiones_matriz)
         
    def resolver_gauss(self):
        try:
            
            self.matriz.matriz = InterfazHelper.procesar_entradas_matrices(self.entradas)
            
            resultado, pasos = self.matriz.eliminacion_gauss_jordan()
            
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            self.resultado_texto= InterfazHelper.mostrar_resultados(
                f"Soluciones:\n{self.matriz.calcular_soluciones_general()}\n\nResultado:\n{self.matriz.mostrar()}\n\nPasos:\n{pasos}"
            )
            
            self.main_layout.addWidget(self.resultado_texto)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

class OperacionesVectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Vectores")
        self.setGeometry(100, 100, 500, 600)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        self.dimension_input = QLineEdit()
        self.vector_inputs = []
        self.escalar_inputs = []
        self.resultado_texto = None
        self.contenedor_vectores_layout = None

        contenedor_layout, self.contenedor_vectores_layout, self.contenedor_botones_layout = InterfazHelper.crear_layout_vectores(
            n_input=self.dimension_input,
            ingresar_dimension_callback=lambda: InterfazHelper.ingresar_vectores(dimension_input=self.dimension_input,
                                                                        vector_inputs=self.vector_inputs,
                                                                        escalar_inputs=self.escalar_inputs,
                                                                        contenedor_vectores_layout=self.contenedor_vectores_layout,
                                                                        contenedor_botones_layout=self.contenedor_botones_layout,
                                                                        ejecutar_callback=self.ejecutar_operacion
            )
        )

        self.main_layout.addLayout(contenedor_layout)
                
    def ejecutar_operacion(self):
        try:
            lista_vectores = InterfazHelper.leer_entrada_vectores_escalares(self.vector_inputs, self.escalar_inputs)
            if not lista_vectores:
                return 
            
            resultado, pasos = Vector.sumar_vectores(*lista_vectores)
            
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)

            self.resultado_texto = InterfazHelper.mostrar_resultados(pasos)

            self.main_layout.addWidget(self.resultado_texto)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class ProductoVectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Producto de Vector Fila por Vector Columna")
        self.setGeometry(100, 100, 500, 400)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.dimension_input = QLineEdit()
        self.vector_fila_inputs = [] 
        self.vector_columna_inputs = []
        self.escalares_inputs = []
        self.resultados_texto = None

        contenedor_layout, self.contenedor_vectores_layout, self.contenedor_botones_layout = InterfazHelper.crear_layout_vectores(
            n_input=self.dimension_input,
            ingresar_dimension_callback=self.ingresar_vectores_fila_columna
        )
        
        self.main_layout.addLayout(contenedor_layout)

    def ingresar_vectores_fila_columna(self):

        InterfazHelper.limpiar_entradas_vectores(self.vector_columna_inputs, self.escalares_inputs, self.contenedor_vectores_layout)        
        InterfazHelper.limpiar_entradas_vectores(self.vector_fila_inputs, self.escalares_inputs, self.contenedor_vectores_layout)        

        

        n = InterfazHelper.leer_entrada_dimension_vector(self.dimension_input)

        if n is None:
                return

        InterfazHelper.agregar_campo_vector(self.vector_fila_inputs, self.escalares_inputs, self.contenedor_vectores_layout, n, orientacion="horizontal")
        InterfazHelper.agregar_campo_vector(self.vector_columna_inputs, self.escalares_inputs, self.contenedor_vectores_layout, n, orientacion="vertical")

        if self.contenedor_botones_layout.count() == 0:
            ejecutar_btn = QPushButton("Calcular producto")
            ejecutar_btn.clicked.connect(self.calcular_producto)
            self.contenedor_botones_layout.addWidget(ejecutar_btn)
    
    def procesar_entrada_vectores(self):
        try:
            
            valores_escalares = [escalar[0][1] for escalar in self.escalares_inputs]
            vector_fila_obj = InterfazHelper.procesar_entrada(self.vector_fila_inputs, [valores_escalares[0]], "horizontal")[0]
            vector_columna_obj = InterfazHelper.procesar_entrada(self.vector_columna_inputs, [valores_escalares[1]], "vertical")[0]
            
            return vector_fila_obj, vector_columna_obj

        except ValueError as e:
            QMessageBox.critical(self, "Error al procesar entradas", str(e))
            return []

    def calcular_producto(self):
        try:
        
            vector_fila_obj, vector_columna_obj = self.procesar_entrada_vectores()
            
            resultado, pasos = vector_fila_obj.producto_vector_fila_por_vector_columna(vector_columna_obj)

            InterfazHelper.limpiar_resultados_texto(self.resultados_texto, self.main_layout)

            self.resultados_texto = InterfazHelper.mostrar_resultados(f"{pasos}\nResultado del producto: {resultado}")

            self.main_layout.addWidget(self.resultados_texto)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

class TransformacionMatrizVisualizadorWidget(QDialog):
    def __init__(self, visualizador):
        super().__init__()

        self.visualizador = visualizador
        self.setWindowTitle("Visualización de Transformación")

        layout = QVBoxLayout(self)

        # Configuración de matplotlib para PyQt
        self.fig, self.ax = plt.subplots(figsize=(8, 6))  # Tamaño ajustado
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.canvas.mpl_connect('scroll_event', self.zoom)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)  # Slider de 0 a 100 para representar t entre 0 y 1
        self.slider.setValue(0)  # Valor inicial del slider
        self.slider.setSingleStep(1)  # Incrementos de 0.01
        self.slider.valueChanged.connect(self.actualizar_transformacion)

        # Crear etiqueta para mostrar el valor de t
        self.label = QLabel(f't = 0.00')
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        # Almacenar las referencias de los textos creados
        self.text_objects = []

        # Visualización inicial con t = 0 (sin transformación)
        self.actualizar_transformacion()
        self.exec_()

    def actualizar_transformacion(self):
        t = self.slider.value() / 100.0
        self.label.setText(f't = {t:.2f}')
        self.ax.clear()  # Limpia la gráfica, pero no los textos fuera del eje

        # Limpiar los textos anteriores
        for text_obj in self.text_objects:
            text_obj.remove()
        self.text_objects = []

        # Visualizamos la transformación
        self.visualizador.visualizar_con_interpolacion(self.ax, rango_valores=20, paso=1, t=t)

        # Establecemos los límites de los ejes
        self.ax.set_xlim(-7, 7)
        self.ax.set_ylim(-7, 7)

        # Fuentes personalizadas
        font_x1 = {'family': 'courier new',  
                'color': 'red', 
                'weight': 'bold',  
                'size': 10} 

        font_x2 = {'family': 'courier new',  
                'color': 'green', 
                'weight': 'bold', 
                'size': 10}  
     
        font_vector = {'family': 'courier new',  
                'color': 'yellow', 
                'weight': 'bold', 
                'size': 10} 
        
        font_resultado = {'family': 'courier new',  
                'color': 'white', 
                'weight': 'bold', 
                'size': 10}  
        
        espaciado_fijo = 0.02 

        x_base = 0.25

        def formatear_numero(num):
            return f'{num:6.2f}'  

        def calcular_longitud_texto(texto):

            return len(texto) * 0.01

        matriz_0_0_str = formatear_numero(self.visualizador.matriz.matriz[0][0])
        matriz_1_0_str = formatear_numero(self.visualizador.matriz.matriz[1][0])
        self.text_objects.append(self.fig.text(x_base, 0.8, f'[{matriz_0_0_str}\n[{matriz_1_0_str}', fontdict=font_x1))

        longitud_columna1 = calcular_longitud_texto(matriz_0_0_str)
        x_base = x_base + longitud_columna1 + 0.01

        matriz_0_1_str = formatear_numero(self.visualizador.matriz.matriz[0][1])
        matriz_1_1_str = formatear_numero(self.visualizador.matriz.matriz[1][1])
        self.text_objects.append(self.fig.text(x_base, 0.8, f'{matriz_0_1_str}]\n{matriz_1_1_str}]', fontdict=font_x2))

        longitud_columna2 = calcular_longitud_texto(matriz_0_1_str)
        x_base = x_base + longitud_columna2 + espaciado_fijo

        vector_0_str = formatear_numero(self.visualizador.vector.vector[0])
        vector_1_str = formatear_numero(self.visualizador.vector.vector[1])
        self.text_objects.append(self.fig.text(x_base, 0.8, f'[{vector_0_str}]\n[{vector_1_str}]', fontdict=font_vector))

        longitud_vector = calcular_longitud_texto(vector_0_str)
        x_base = x_base + longitud_vector + espaciado_fijo

        self.text_objects.append(self.fig.text(x_base, 0.82, ' = ', fontdict=font_resultado))

        longitud_igual = calcular_longitud_texto('=')
        x_base = x_base + longitud_igual + espaciado_fijo

        resultado_0_str = formatear_numero(self.visualizador.resultado[0])
        resultado_1_str = formatear_numero(self.visualizador.resultado[1])
        self.text_objects.append(self.fig.text(x_base, 0.8, f'[{resultado_0_str}]\n[{resultado_1_str}]', fontdict=font_resultado))

        self.canvas.draw()

    def zoom(self, event):
        base_scale = 1.2

        if event.button == 'up':
            scale_factor = base_scale
        elif event.button == 'down':
            scale_factor = 1 / base_scale
        else:
            return
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        xdata = event.xdata  # Obtener la posición del mouse en x
        ydata = event.ydata  # Obtener la posición del mouse en y
        if xdata is None or ydata is None:
            return
        new_xlim = [xdata - (xdata - xlim[0]) / scale_factor, xdata + (xlim[1] - xdata) / scale_factor]
        new_ylim = [ydata - (ydata - ylim[0]) / scale_factor, ydata + (ylim[1] - ydata) / scale_factor]

        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw()
            
class MultiplicacionMatrizVectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)  # Aumentar tamaño de la ventana para más espacio
        self.setWindowTitle("Multiplicación de Matriz por Vector")

        # Layout principal vertical
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        #Nivel 1
        self.contenedor_inputs = QHBoxLayout()
        self.main_layout.addLayout(self.contenedor_inputs)
        self.resultado_texto = None
        
        #Nivel 2
        self.contenedor_matriz = QVBoxLayout()
        self.contenedor_vector = QHBoxLayout()
        self.contenedor_ejecutar = QHBoxLayout()

        self.contenedor_inputs.addLayout(self.contenedor_matriz)
        self.contenedor_inputs.addLayout(self.contenedor_vector)
        self.contenedor_inputs.addLayout(self.contenedor_ejecutar)

        #Nivel 3
        self.n_input = QLineEdit()
        self.m_input = QLineEdit()

        layout_dimensiones_matriz = InterfazHelper.crear_layout_ingresar_dimensiones(
                labels_inputs=[("Filas de la matriz:", self.n_input), ("Columnas de la matriz:", self.m_input)],
                boton_texto="Ingresar Matriz",
                boton_callback=lambda: InterfazHelper.ingresar_matriz(instancia=self,
                                                                      main_layout=self.contenedor_matriz,
                                                                      resultado_texto=self.resultado_texto,
                                                                      grid_layout=self.grid_layout,
                                                                      n_input=self.n_input,
                                                                      m_input=self.m_input,
                                                                      calcular_callback=self.guardar_matriz,
                                                                      nombre_boton="Guardar matriz",
                                                                      target_layout=self.contenedor_matriz,
                                                                      rectangular=True
                                                                    )
        )
        self.contenedor_matriz.addLayout(layout_dimensiones_matriz)

        self.dimension_vectores_input = QLineEdit()

        contenedor_layout, self.contenedor_vectores_layout, self.contenedor_botones_layout = InterfazHelper.crear_layout_vectores(
            n_input=self.dimension_vectores_input,
            ingresar_dimension_callback=self.ingresar_vectores
        )
        self.contenedor_vector.addLayout(contenedor_layout)

        # Matriz y vector que se multiplicaran al final
        self.matriz = None
        self.vector_columna = None

        self.grid_layout = None
        self.rectangular = True
        self.entradas = []
        self.calc_botones_layout = QHBoxLayout()
        self.vector_inputs = []
        self.escalar_inputs = []
        self.opciones_calc_combo_box = QComboBox()
        self.opciones_calc_combo_box.addItems(["","Calcular multiplicacion", "Demostrar propiedad distributiva"])

        # Añadir el botón de calcular al final del main_layout
        calcular_btn = QPushButton("Calcular")
        calcular_btn.clicked.connect(self.calc_respuesta)
        self.calc_botones_layout.addWidget(calcular_btn)
        self.calc_botones_layout.addWidget(self.opciones_calc_combo_box)
        self.main_layout.addLayout(self.calc_botones_layout)

    def ingresar_vectores(self):
       
        n = InterfazHelper.leer_entrada_dimension_vector(self.dimension_vectores_input)

        if n is None:
            return  

        InterfazHelper.crear_botones_vectores(lambda: InterfazHelper.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout, n),
                                              lambda: InterfazHelper.eliminar_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout),
                                              lambda: self.calcular_vector_columna(), 
                                              self.contenedor_botones_layout  
                                              )

        InterfazHelper.limpiar_entradas_vectores(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout)

        InterfazHelper.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout,n)
        InterfazHelper.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout,n)


    def guardar_matriz(self):
        try:
            
            self.matriz.matriz = InterfazHelper.procesar_entradas_matrices(self.entradas)
            
            QMessageBox.information(self, "Éxito", "Los valores de la matriz han sido guardados correctamente.")

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

    def procesar_entrada_vectores(self):
        try:
            
            valores_vector = [elemento for elemento in self.vector_inputs]        
            valores_escalar = [entrada[0][1] for entrada in self.escalar_inputs]

            lista_vectores_escalados = InterfazHelper.procesar_entrada(valores_vector, valores_escalar)

            return lista_vectores_escalados

        except ValueError as e:
            QMessageBox.critical(self, "Error al procesar entradas", str(e))
            return []


    def calcular_vector_columna(self):
        try:
            lista_vectores = self.procesar_entrada_vectores()
            if not lista_vectores:
                return 
            
            resultado, pasos = Vector.sumar_vectores(*lista_vectores)
        
            self.vector_columna = resultado

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_respuesta(self):
        
        try:
            opcion_seleccionada = self.opciones_calc_combo_box.currentText()
            
            if opcion_seleccionada == "Calcular multiplicacion":
                self.realizar_multiplicacion_matriz_vector()
            elif opcion_seleccionada == "Demostrar propiedad distributiva":
                self.realizar_multiplicacion_con_demostracion_distributiva()
            elif opcion_seleccionada == "Visualizar transformacion":
                if not hasattr(self, 'matriz') or not hasattr(self, 'vector_columna'):
                    raise ValueError("La matriz y el vector deben estar correctamente definidos antes de visualizar la transformación.")
    
                self.visualizador = VisualizadorMatrizPorVector(self.matriz, self.vector_columna)
                TransformacionMatrizVisualizadorWidget(self.visualizador)
            else:
                print("Ingrese una opcion válida")        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al ejecutar la operación: {str(e)}")

    def realizar_multiplicacion_matriz_vector(self):
        try:
            # Verificar si la matriz y el vector columna están correctamente definidos
            if not hasattr(self, 'matriz') or not self.vector_columna:
                raise ValueError("Debe ingresar la matriz y calcular el vector antes de realizar la multiplicación.")

            # Verificar la compatibilidad de las dimensiones entre la matriz y el vector
            if len(self.matriz.matriz[0]) != len(self.vector_columna.vector):
                raise ValueError("El número de columnas de la matriz debe coincidir con la longitud del vector.")

            # Realizar la multiplicación de la matriz por el vector
            resultado_final, pasos_final = self.matriz.multiplicar_matriz_por_vector(self.vector_columna)

            # Construir el texto de los resultados
            resultado_texto = f"Resultado de la multiplicación de matriz por vector:\n{resultado_final}\n\n"
            pasos_texto = "Pasos detallados de la multiplicación:\n" + pasos_final

            # Mostrar el resultado y los pasos usando InterfazHelper
            resultado_completo = resultado_texto + pasos_texto
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            self.resultado_texto = InterfazHelper.mostrar_resultados(resultado_completo)
            self.main_layout.addWidget(self.resultado_texto)

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

class OperacionesMatrizDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Matrices")
        self.setGeometry(100, 100, 600, 700)

        # Layout principal
        self.main_layout = QVBoxLayout()

        # Inputs para dimensiones de la matriz
        self.n_input = QLineEdit()
        self.m_input = QLineEdit()
        self.rectangular = True  # Indicador para tipo de matriz

        if self.rectangular:
            self.crear_layout_top(
                labels_inputs=[("Filas de la matriz:", self.n_input), ("Columnas de la matriz:", self.m_input)],
                boton_texto="Ingresar Dimensiones",
                boton_callback=self.configurar_matriz
            )
        else:
            self.crear_layout_top(
                labels_inputs=[("Número de ecuaciones:", self.n_input)],
                boton_texto="Ingresar Dimensiones",
                boton_callback=self.configurar_matriz
            )

        # Lista de entradas de matrices y escalares
        self.matriz_inputs = []
        self.escalar_inputs = []

        # Área para las matrices
        self.inputs_layout = QVBoxLayout()
        self.main_layout.addLayout(self.inputs_layout)

        # Botón para agregar matrices
        agregar_btn = QPushButton("Agregar Matriz")
        agregar_btn.clicked.connect(self.agregar_matriz)
        self.main_layout.addWidget(agregar_btn)
        agregar_btn.setEnabled(False)  # Deshabilitado hasta que se configuren las dimensiones
        self.agregar_btn = agregar_btn

        # Botón para eliminar la última matriz
        eliminar_btn = QPushButton("Eliminar Última Matriz")
        eliminar_btn.clicked.connect(self.eliminar_matriz)
        self.main_layout.addWidget(eliminar_btn)

        # Botón para ejecutar la operación
        ejecutar_btn = QPushButton("Ejecutar Suma de Matrices")
        ejecutar_btn.clicked.connect(self.ejecutar_operacion)
        self.main_layout.addWidget(ejecutar_btn)

        # Área de texto para mostrar resultados
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        self.resultado_texto.setFontFamily("Courier New")  # Fuente monoespaciada
        self.main_layout.addWidget(self.resultado_texto)

        self.setLayout(self.main_layout)

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

    def configurar_matriz(self):
        try:
            filas = int(self.n_input.text())
            columnas = int(self.m_input.text()) if self.rectangular else int(self.n_input.text())
            if filas <= 0 or columnas <= 0:
                raise ValueError("Las dimensiones deben ser enteros positivos.")

            # Configurar el tamaño de las matrices
            self.filas = filas
            self.columnas = columnas
            self.agregar_btn.setEnabled(True)  # Habilitar el botón para agregar matrices

            # Agregar automáticamente dos matrices con las dimensiones especificadas
            self.agregar_matriz()
            self.agregar_matriz()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def agregar_matriz(self):
        layout = QVBoxLayout()

        titulo_layout = QHBoxLayout()
        titulo = QLabel(f"Matriz {len(self.matriz_inputs) + 1}")
        titulo_layout.addWidget(titulo)

        escalar_input = QLineEdit()
        escalar_input.setPlaceholderText("Escalar")
        titulo_layout.addWidget(escalar_input)
        self.escalar_inputs.append(escalar_input)

        layout.addLayout(titulo_layout)

        grid_layout = QGridLayout()
        filas, columnas = self.filas, self.columnas  # Usar las dimensiones configuradas por el usuario
        matriz_entradas = []

        for i in range(filas):
            fila_entradas = []
            for j in range(columnas):
                entrada = QLineEdit()
                entrada.setPlaceholderText(f"({i+1},{j+1})")
                grid_layout.addWidget(entrada, i, j)
                fila_entradas.append(entrada)
            matriz_entradas.append(fila_entradas)

        layout.addLayout(grid_layout)
        layout.setSpacing(15)  # Espaciado para separar las matrices claramente
        self.matriz_inputs.append(matriz_entradas)
        self.inputs_layout.addLayout(layout)

    def eliminar_matriz(self):
        if self.matriz_inputs:
            # Remover los campos de entrada
            matriz_entradas = self.matriz_inputs.pop()
            escalar_input = self.escalar_inputs.pop()
            escalar_input.deleteLater()

            for fila_entradas in matriz_entradas:
                for entrada in fila_entradas:
                    entrada.deleteLater()
            # Remover el layout
            layout = self.inputs_layout.takeAt(len(self.matriz_inputs))
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                self.inputs_layout.removeItem(layout)

    def procesar_entrada_matrices(self):
        try:
            matrices = []
            for idx, matriz_entradas in enumerate(self.matriz_inputs):
                filas = len(matriz_entradas)
                columnas = len(matriz_entradas[0])
                matriz = []
                for i in range(filas):
                    fila = []
                    for j in range(columnas):
                        valor_texto = matriz_entradas[i][j].text()
                        if valor_texto.strip() == "":
                            raise ValueError(f"El elemento ({i+1},{j+1}) de la matriz {idx + 1} está vacío.")
                        valor = float(valor_texto)
                        fila.append(valor)
                    matriz.append(fila)
                
                matriz_obj = Matriz(filas, columnas, matriz)
                escalar_texto = self.escalar_inputs[idx].text()
                if escalar_texto.strip():
                    escalar = float(escalar_texto)
                    matriz_obj = matriz_obj.escalar_matriz(escalar)
                
                matrices.append(matriz_obj)
            return matrices
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return []  # Retornar una lista vacía en caso de error

    def ejecutar_operacion(self):
        try:
            # Llamar a procesar_entrada_matrices para obtener la lista de objetos Matriz
            lista_matrices = self.procesar_entrada_matrices()
            if not lista_matrices:
                return

            resultado, pasos = Matriz.sumar_matrices(*lista_matrices)

            # Mostrar el resultado de la suma de matrices
            self.resultado_texto.setText(pasos)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
class MultiplicacionMatricesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Matrices")
        self.setGeometry(100, 100, 800, 400)

        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignTop)

        # Nivel 1

        self.inputs_layout= QVBoxLayout()
        self.resultado_texto = None

        self.main_layout.addLayout(self.inputs_layout)

        self.n_inputs = [QLineEdit(), QLineEdit()]
        self.m_inputs = [QLineEdit(), QLineEdit()]
        self.grid_layout_matrices = []
        self.entradas_matrices = []
        self.matrices = []

        layout_dimensiones_matriz_1 = InterfazHelper.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Filas de la Matriz 1:", self.n_inputs[0]),("Columnas de la Matriz 1:", self.m_inputs[0]), 
                           ("Filas de la Matriz 2:", self.n_inputs[1]),("Columnas de la Matriz 2:", self.m_inputs[1])],
            boton_texto="Ingresar Matrices",
            boton_callback=lambda: InterfazHelper.ingresar_multiples_matrices(instancia=self,
                                                                            main_layout=self.main_layout,
                                                                            resultado_texto=self.resultado_texto,
                                                                            grid_layouts=self.grid_layout_matrices,
                                                                            n_inputs=self.n_inputs,
                                                                            m_inputs=self.m_inputs,
                                                                            nombre_boton="Multiplicar matrices",
                                                                            operacion_callback=self.multiplicar_matrices,
                                                                            target_layout=self.inputs_layout
            )

        )

        self.main_layout.addLayout(layout_dimensiones_matriz_1)
    
       # Checkboxes para transponer matrices
        self.transponer_matriz1_checkbox = QCheckBox("Transponer primera matriz")
        self.transponer_matriz2_checkbox = QCheckBox("Transponer segunda matriz")
        self.transponer_resultado_checkbox = QCheckBox("Transponer resultado final")
        self.main_layout.addWidget(self.transponer_matriz1_checkbox)
        self.main_layout.addWidget(self.transponer_matriz2_checkbox)
        self.main_layout.addWidget(self.transponer_resultado_checkbox)

        # Área para las matrices
        self.inputs_layout = QHBoxLayout()
        self.main_layout.addLayout(self.inputs_layout)

    def multiplicar_matrices(self):
        try:
            lista_matrices = []

            for indx, matriz in enumerate(self.matrices):
                matriz.matriz = InterfazHelper.procesar_entradas_matrices(self.entradas_matrices[indx])
                lista_matrices.append(matriz)
            
            if len(lista_matrices) != 2:
                QMessageBox.warning(self, "Error", "Debe ingresar dos matrices para multiplicarlas.")
                return

            pasos = ""

            if self.transponer_matriz1_checkbox.isChecked():
                pasos += "Matriz 1 original:\n" + lista_matrices[0].mostrar() + "\n"
                lista_matrices[0] = Matriz.transponer_matriz(lista_matrices[0])
                pasos += "Matriz 1 transpuesta:\n" + lista_matrices[0].mostrar() + "\n"
            if self.transponer_matriz2_checkbox.isChecked():
                pasos += "Matriz 2 original:\n" + lista_matrices[1].mostrar() + "\n"
                lista_matrices[1] = Matriz.transponer_matriz(lista_matrices[1])
                pasos += "Matriz 2 transpuesta:\n" + lista_matrices[1].mostrar() + "\n"

            # Multiplicar
            resultado, pasos_multiplicacion = lista_matrices[0].multiplicar_matrices(lista_matrices[1])
            pasos += pasos_multiplicacion

            if self.transponer_resultado_checkbox.isChecked():
                resultado = Matriz.transponer_matriz(resultado)
                pasos += "\nResultado transpuesto:\n" + resultado.mostrar()


            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            self.resultado_texto = InterfazHelper.mostrar_resultados(pasos)

            self.main_layout.addWidget(self.resultado_texto)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class DeterminanteDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Ingresar Matriz")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        self.entradas = []
        self.grid_layout = None
        self.resultado_texto = None
        self.placeholder_respuestas = None
        self.matriz = None
        
        self.n_input = QLineEdit()
        self.m_input = self.n_input
         
        layout_dimensiones_matriz = InterfazHelper.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Dimensiones de la matriz:", self.n_input)],
            boton_texto="Ingresar Matriz",
            boton_callback=lambda: InterfazHelper.ingresar_matriz(instancia=self,
                                                                  main_layout=self.main_layout,
                                                                  resultado_texto=self.resultado_texto,
                                                                  grid_layout=self.grid_layout, 
                                                                  n_input=self.n_input, 
                                                                  m_input=self.m_input,
                                                                  calcular_callback=self.calcular_determinante, 
                                                                  nombre_boton="Calcular determinante",
                                                                  rectangular=True,
                                                                  target_layout=self.main_layout
                                                                )
         )
        
        self.main_layout.addLayout(layout_dimensiones_matriz) 
    
    def calcular_determinante(self):
        try:
            self.matriz.matriz = InterfazHelper.procesar_entradas_matrices(self.entradas)
            
            det, pasos = self.matriz.calcular_determinante()
            
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            self.resultado_texto = InterfazHelper.mostrar_resultados(
                f"Determinante:\n{det}\n\nPasos:\n{pasos}"
            )
    
            self.main_layout.addWidget(self.resultado_texto)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

class CramerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resolver Sistema por Regla de Cramer")
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
    
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.n_input = QLineEdit()
        self.n_input.setPlaceholderText("Número de ecuaciones (n)")
        self.grid_layout = None


        layout_dimensiones = InterfazHelper.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Número de ecuaciones:", self.n_input)],
            boton_texto="Configurar Matriz",
            boton_callback=lambda: InterfazHelper.configurar_matriz_y_vector(instancia=self,
                                                                  main_layout=self.main_layout,
                                                                  resultado_texto=self.resultado_texto,
                                                                  grid_layout=self.grid_layout, 
                                                                  n_input=self.n_input, 
                                                                  calcular_callback=self.calcular_cramer, 
                                                                  nombre_boton="Calcular por regla de Cramer",
                                                                  target_layout=self.main_layout,
                                                                )
         
        )
        
        self.main_layout.addLayout(layout_dimensiones)
        
        self.layout_grid = None
        self.resultado_texto = None
        
        self.entradas_matriz = []
        self.entradas_vector = []

    def calcular_cramer(self):
        try:
        
            matriz_valores = InterfazHelper.procesar_entradas_matrices(self.entradas_matriz)
            vector_constantes = [float(entrada.text()) for entrada in self.entradas_vector]

            matriz = Matriz(len(matriz_valores), len(matriz_valores), matriz_valores)
            soluciones, mensaje_o_pasos = matriz.resolver_cramer(vector_constantes)
            
            if soluciones is None:
                QMessageBox.warning(self, "Sin solución", mensaje_o_pasos)
            else:
                texto_resultado = "\n".join([f"x{i+1} = {sol}" for i, sol in enumerate(map(str, soluciones))])

                InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
                resultado_texto_widget = InterfazHelper.mostrar_resultados(f"Soluciones:\n{texto_resultado}\n\nPasos:\n{mensaje_o_pasos}")
                
                self.main_layout.addWidget(resultado_texto_widget)
                self.resultado_texto = resultado_texto_widget

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

class InversaDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Ingresar Matriz")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        self.entradas = []
        self.grid_layout = None
        self.resultado_texto = None
        self.placeholder_respuestas = None
        self.matriz:Matriz = None
        
        self.n_input = QLineEdit()
        self.m_input = self.n_input
         
        layout_dimensiones_matriz = InterfazHelper.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Dimensiones de la matriz:", self.n_input)],
            boton_texto="Ingresar Matriz",
            boton_callback=lambda: InterfazHelper.ingresar_matriz(instancia=self,
                                                                  main_layout=self.main_layout,
                                                                  resultado_texto=self.resultado_texto,
                                                                  grid_layout=self.grid_layout, 
                                                                  n_input=self.n_input, 
                                                                  m_input=self.m_input,
                                                                  calcular_callback=self.calcular_inversa, 
                                                                  nombre_boton="Calcular matriz Inversa",
                                                                  target_layout=self.main_layout,
                                                                  rectangular=True
                                                                )
         )
        
        self.main_layout.addLayout(layout_dimensiones_matriz)
         
    def calcular_inversa(self):
        try:
            self.matriz.matriz = InterfazHelper.procesar_entradas_matrices(self.entradas)
            
            matriz_inversa, pasos = self.matriz.calcular_inversa()
            
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            
            # Mostrar el determinante en la interfaz
        
            # Mostrar el determinante en la interfaz
            self.resultado_texto = InterfazHelper.mostrar_resultados(
                f"Matriz inversa:\n{matriz_inversa.mostrar()}\n\nPasos:\n{pasos}"
            )
            
            self.main_layout.addWidget(self.resultado_texto)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error",f"{str(e)}")


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
        self.multiplicacion_matriz_vector_btn = QPushButton("Multiplicación de Matriz por Vector")
        self.multiplicacion_matriz_vector_btn.clicked.connect(self.mostrar_multiplicacion_matriz_vector_dialog)
        self.layout.addWidget(self.multiplicacion_matriz_vector_btn)
        self.operaciones_matrices_btn = QPushButton("Operaciones con Matrices")
        self.operaciones_matrices_btn.clicked.connect(self.mostrar_operaciones_matrices_dialog)
        self.layout.addWidget(self.operaciones_matrices_btn)
        self.multiplicar_matrices_btn = QPushButton("Multiplicar Matrices")
        self.multiplicar_matrices_btn.clicked.connect(self.mostrar_multiplicacion_matrices_dialog)
        self.layout.addWidget(self.multiplicar_matrices_btn)
        self.determinantes_btn = QPushButton("Calcular Determinante")
        self.determinantes_btn.clicked.connect(self.mostrar_determinante_dialog)
        self.layout.addWidget(self.determinantes_btn)
        self.cramer_btn = QPushButton("Regla de Cramer")
        self.cramer_btn.clicked.connect(self.mostrar_cramer_dialog)
        self.layout.addWidget(self.cramer_btn)
        self.inversa_btn = QPushButton("Matriz Inversa")
        self.inversa_btn.clicked.connect(self.mostrar_inversa_dialog)
        self.layout.addWidget(self.inversa_btn)
        
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
        
    def mostrar_multiplicacion_matriz_vector_dialog(self):
        dialog = MultiplicacionMatrizVectorDialog()
        dialog.exec_()
        
    def mostrar_operaciones_matrices_dialog(self):
        dialog = OperacionesMatrizDialog()
        dialog.exec_()
        
    def mostrar_multiplicacion_matrices_dialog(self):
        dialog = MultiplicacionMatricesDialog()
        dialog.exec_()
    
    def mostrar_determinante_dialog(self):
        dialog = DeterminanteDialog()
        dialog.exec_()

    def mostrar_cramer_dialog(self):
        dialog = CramerDialog()
        dialog.exec_()
    
    def mostrar_inversa_dialog(self):
        dialog = InversaDialog()
        dialog.exec_()


# Iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())