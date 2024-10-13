import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSpacerItem, QSizePolicy, QMessageBox, QTextEdit, QMainWindow, QWidget, QComboBox,QSlider, QCheckBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matrices import Matriz
from vectores import Vector
from utilidades import *
from visualizador import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Subclase personalizada de QLineEdit para manejar eventos de Enter correctamente
class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            event.accept()  # Ignorar el evento de Enter para que no cause efectos secundarios
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
    def limpiar_grid_layout(grid_layout, main_layout):
         if grid_layout is not None:
            while grid_layout.count():
                widget = grid_layout.takeAt(0).widget()
                if widget is not None:
                    widget.deleteLater()
            main_layout.removeItem(grid_layout)
        
    @staticmethod
    def configurar_grid_layout(n, m, aceptar_callback):
 
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

        aceptar_btn = QPushButton("Aceptar")
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
        contenedor_vectores_layout = QHBoxLayout()
        
        dimension_layout = InterfazHelper.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Dimensión de los vectores:", n_input)],
            boton_texto="Ingresar dimensión",
            boton_callback=ingresar_dimension_callback  # Conectar el botón al callback de ingresar vectores
        )

        contenedor_vectores_layout.addLayout(dimension_layout)

        contenedor_layout.addLayout(contenedor_vectores_layout)

        return contenedor_layout, contenedor_vectores_layout
        
    @staticmethod
    def crear_botones_vectores(agregar_vector_callback, eliminar_vector_callback, ejecutar_operacion_callback, contenedor_layout):
        
        agregar_btn = QPushButton("Agregar Vector")
        agregar_btn.clicked.connect(agregar_vector_callback)
        contenedor_layout.addWidget(agregar_btn)
        
        eliminar_btn = QPushButton("Eliminar Último Vector")
        eliminar_btn.clicked.connect(eliminar_vector_callback)
        contenedor_layout.addWidget(eliminar_btn)
        
        ejecutar_btn = QPushButton("Ejecutar Operación")
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
    def crear_entrada_vector(dimension):
        contenedor_vectores_inputs=QVBoxLayout()
        escalar_input_layout=QHBoxLayout()
        
        label= QLabel("Escalar del vector:")
        escalar_input= QLineEdit()
        escalar_input_layout.addWidget(label)
        escalar_input_layout.addWidget(escalar_input)
        
        grid_layout = QGridLayout()
        entradas_vector = []

        for i in range(dimension):
            
            etiqueta = QLabel(f"Componente {i + 1}:")
            grid_layout.addWidget(etiqueta, i, 0)

            entrada = QLineEdit()
            entrada.setPlaceholderText(f"Valor {i + 1}")
            grid_layout.addWidget(entrada, i, 1)

            entradas_vector.append(entrada)
        
        contenedor_vectores_inputs.addLayout(escalar_input_layout)
        contenedor_vectores_inputs.addLayout(grid_layout)
        
        return escalar_input, entradas_vector, contenedor_vectores_inputs
    
    @staticmethod
    def agregar_campo_vector(vector_inputs, escalar_inputs, layout, n):
        
        entrada_escalar, entrada_vector, contenedor_entradas_vector = InterfazHelper.crear_entrada_vector(n)
        
        layout.addLayout(contenedor_entradas_vector)
        
        vector_inputs.append(entrada_vector)
        escalar_inputs.append(entrada_escalar)
    
    @staticmethod    
    def eliminar_vector(vector_inputs, escalar_inputs, inputs_layout):
        if vector_inputs:
        
            entradas_vector = vector_inputs.pop()
            escalar_input = escalar_inputs.pop()

            escalar_input.deleteLater()

            for entrada in entradas_vector:
                entrada.deleteLater()

            layout = inputs_layout.takeAt(len(vector_inputs))
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                inputs_layout.removeItem(layout)
                
    
        
    
    
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
        self.matriz = None
        
        # Inputs para dimensiones de la matriz
        self.n_input = QLineEdit()
        self.m_input = QLineEdit()
         
        if self.rectangular:
            
            layout_dimensiones_matriz = InterfazHelper.crear_layout_ingresar_dimensiones(
                labels_inputs=[("Filas de la matriz:", self.n_input), ("Columnas de la matriz:", self.m_input)],
                boton_texto="Ingresar Matriz",
                boton_callback=lambda: self.ingresar_matriz()
                )
        else:
            layout_dimensiones_matriz = InterfazHelper.crear_layout_ingresar_dimensiones(
                labels_inputs=[("Número de ecuaciones:", self.n_input)],
                boton_texto="Ingresar Matriz",
                boton_callback=lambda: self.ingresar_matriz()
            )

        self.main_layout.addLayout(layout_dimensiones_matriz)
         
    def ingresar_matriz(self):
        try:
            
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            InterfazHelper.limpiar_grid_layout(self.grid_layout, self.main_layout)
            
            n, m = InterfazHelper.leer_entradas_dimensiones_matrices(self.n_input, self.m_input, self.rectangular)
            
            self.matriz = Matriz(n,m)
            
            self.grid_layout, self.entradas=InterfazHelper.configurar_grid_layout(n, m, self.ejecutar_operacion)
        
            self.main_layout.addLayout(self.grid_layout)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")
        

    def ejecutar_operacion(self):
        try:
            
            self.matriz.matriz = InterfazHelper.procesar_entradas_matrices(self.entradas)
            
            resultado, pasos, soluciones = self.matriz.eliminacion_gauss_jordan()
            
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            self.resultado_texto= InterfazHelper.mostrar_resultados(
                f"Soluciones:\n{soluciones}\n\nResultado:\n{self.matriz.mostrar()}\n\nPasos:\n{pasos}"
            )
            
            self.main_layout.addWidget(self.resultado_texto)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

class OperacionesVectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Vectores")
        self.setGeometry(100, 100, 500, 600)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        
        self.setLayout(self.main_layout)
        
        self.dimension_input = QLineEdit()
        self.vector_inputs = []
        self.escalar_inputs = []
        
        contenedor_layout, self.contenedor_vectores_layout = InterfazHelper.crear_layout_vectores(
            n_input=self.dimension_input,
            ingresar_dimension_callback=self.ingresar_vectores
        )

        self.main_layout.addLayout(contenedor_layout)
                
        """
        # Botón para agregar vectores
        agregar_btn = QPushButton("Agregar Vector")
        agregar_btn.clicked.connect(InterfazHelper.agregar_campo_vector)
        self.main_layout.addWidget(agregar_btn)

        # Botón para eliminar el último vector
        eliminar_btn = QPushButton("Eliminar Último Vector")
        eliminar_btn.clicked.connect(self.eliminar_vector)
        self.main_layout.addWidget(eliminar_btn)

        # Botón para ejecutar la operación
        ejecutar_btn = QPushButton("Ejecutar Operación")
        ejecutar_btn.clicked.connect(self.ejecutar_operacion)
        self.main_layout.addWidget(ejecutar_btn)"""
        
    def ingresar_vectores(self):
       
        n = InterfazHelper.leer_entrada_dimension_vector(self.dimension_input)

        if n is None:
            return  

        InterfazHelper.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout,n)
        InterfazHelper.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout,n)
        
        InterfazHelper.crear_botones_vectores(InterfazHelper.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout, n),
                                              InterfazHelper.eliminar_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout),
                                              self.ejecutar_operacion(), self.contenedor_vectores_layout  
                                              )
    """
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
                self.inputs_layout.removeItem(layout)"""

    def procesar_entrada_vectores(self):
        try:
            vectores = []
            escalares = []
            for idx, vector_input in enumerate(self.vector_inputs):
                vector_text = vector_input.text()
                if vector_text.strip() == "":
                    raise ValueError(f"El vector {idx + 1} está vacío.")
                vector = [float(x.strip()) for x in vector_text.split(",")]
                vectores.append(vector)
            
            for idx, escalar_input in enumerate(self.escalar_inputs):
                escalar_text = escalar_input.text()
                escalar = float(escalar_text)
                escalares.append(escalar)

            if len(vectores) != len(escalares):
                raise ValueError("El número de vectores y escalares no coincide.")

            vector_objeto = [Vector(len(vector), vector) for vector in vectores]
            
            # Crear la lista de vectores usando la clase Vector correctamente
            lista_vectores_escalados = [vector_escalado.escalar_vector(escalar) for vector_escalado, escalar in zip(vector_objeto,escalares)]
            return lista_vectores_escalados
        
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return []  # Retornar una lista vacía en caso de error
        
    def ejecutar_operacion(self):
            
        try:
            # Llamar a procesar_entrada_vectores para obtener la lista de objetos Vector
            lista_vectores = self.procesar_entrada_vectores()
            if not lista_vectores:
                return 
            
            resultado, pasos = Vector.sumar_vectores(*lista_vectores)
            
            self.resultado_texto.setText(pasos)

        except Exception as e:
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

            # Obtener los datos de entrada y convertirlos en vectores
            vector_fila_text = self.vector_fila_input.text().strip()
            vector_columna_text = self.vector_columna_input.text().strip()

            if not vector_fila_text or not vector_columna_text:
                raise ValueError("Ambos vectores deben ser proporcionados.")

            vector_fila = [float(x.strip()) for x in vector_fila_text.split(",")]
            vector_columna = [float(x.strip()) for x in vector_columna_text.split(",")]

            # Crear instancias de la clase Vector
            vector_fila_obj = Vector(len(vector_fila), vector_fila, orientacion="horizontal")
            vector_columna_obj = Vector(len(vector_columna), vector_columna, orientacion="vertical")

            # Calcular el producto de vector fila por vector columna usando la nueva función
            resultado, pasos = vector_fila_obj.producto_vector_fila_por_vector_columna(vector_columna_obj)

            # Mostrar el resultado en la interfaz
            resultado_texto = f"{pasos}\nResultado del producto: {resultado}"
            self.resultado_texto.setText(resultado_texto)
            

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
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # Layout horizontal para matriz y vector
        self.horizontal_layout = QHBoxLayout()
        self.grid_layout = None
        self.entradas = []
        self.resultado_texto = None
        self.placeholder_respuestas = None
        self.matriz_layout = QVBoxLayout()
        self.vector_layout = QVBoxLayout()
        self.calc_botones_layout = QHBoxLayout()
        self.vector_inputs = []  # Lista para almacenar entradas de vectores
        self.escalar_inputs = []
        self.opciones_calc_combo_box = QComboBox()
        self.opciones_calc_combo_box.addItems(["","Calcular multiplicacion", "Demostrar propiedad distributiva"])

        # Inputs para dimensiones de la matriz
        self.n_input = QLineEdit()
        self.m_input = QLineEdit()

        # Crear el layout superior para ingresar dimensiones y botón de matriz
        self.crear_layout_top(
            labels_inputs=[("Filas de la matriz:", self.n_input), ("Columnas de la matriz:", self.m_input)],
            boton_texto="Ingresar Matriz",
            boton_callback=self.ingresar_matriz
        )

        # Añadir botones para gestionar vectores al vector_layout
        agregar_vector_btn = QPushButton("Agregar Vector")
        agregar_vector_btn.clicked.connect(self.agregar_vector)
        self.vector_layout.addWidget(agregar_vector_btn)

        eliminar_vector_btn = QPushButton("Eliminar Último Vector")
        eliminar_vector_btn.clicked.connect(self.eliminar_vector)
        self.vector_layout.addWidget(eliminar_vector_btn)

        calcular_vector_btn = QPushButton("Calcular Vector Columna")
        calcular_vector_btn.clicked.connect(self.calcular_vector_columna)
        self.vector_layout.addWidget(calcular_vector_btn)

        # Añadir los layouts de matriz y vector al layout horizontal
        self.horizontal_layout.addLayout(self.matriz_layout)
        self.horizontal_layout.addLayout(self.vector_layout)
        
        # Añadir el layout horizontal al layout principal
        self.main_layout.addLayout(self.horizontal_layout)
        
        # Añadir el botón de calcular al final del main_layout
        calcular_btn = QPushButton("Calcular")
        calcular_btn.clicked.connect(self.calc_respuesta)
        self.calc_botones_layout.addWidget(calcular_btn)
        self.calc_botones_layout.addWidget(self.opciones_calc_combo_box)
        self.main_layout.addLayout(self.calc_botones_layout)
        
        self.placeholder_respuestas = QTextEdit()
        self.placeholder_respuestas.setReadOnly(True)
        self.main_layout.addWidget(self.placeholder_respuestas)
        

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

        # Añadir el top_layout al matriz_layout
        self.matriz_layout.addLayout(top_layout)
        self.stretch_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.matriz_layout.addItem(self.stretch_item)

    def configurar_grid_layout(self, n, m, aceptar_callback):
        # Verificar si ya existe un grid layout previo y eliminarlo
        if self.grid_layout is not None:
            while self.grid_layout.count():
                widget = self.grid_layout.takeAt(0).widget()
                if widget is not None:
                    widget.deleteLater()
            self.matriz_layout.removeItem(self.grid_layout)

        if self.stretch_item is not None:
            self.matriz_layout.removeItem(self.stretch_item)
            self.stretch_item = None

        # Crear un nuevo grid layout y agregarlo al layout principal
        self.grid_layout = QGridLayout()
        self.entradas = []

        for i in range(n):
            fila_entradas = []
            for j in range(m):
                entrada = QLineEdit()
                entrada.setPlaceholderText(f"Coef {i+1},{j+1}")
                fila_entradas.append(entrada)
                self.grid_layout.addWidget(entrada, i, j)
            self.entradas.append(fila_entradas)

        aceptar_btn = QPushButton("Aceptar")
        aceptar_btn.clicked.connect(aceptar_callback)
        self.grid_layout.addWidget(aceptar_btn, n, 0, 1, m)
        self.matriz_layout.addLayout(self.grid_layout)

    def ingresar_matriz(self):
        try:
            n = int(self.n_input.text())
            if n <= 0:
                raise ValueError("El número de filas debe ser un número entero positivo.")

            m = int(self.m_input.text())
            if m <= 0:
                raise ValueError("El número de columnas debe ser un número entero positivo.")

            self.matriz = Matriz(n, m)
            if self.matriz.filas == 2 and self.matriz.columnas == 2:
                self.opciones_calc_combo_box.addItem("Visualizar transformacion")
            self.configurar_grid_layout(n, m, self.procesar_entradas)
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")

    def procesar_entradas(self):
        try:
            # Crear una matriz temporal para almacenar los valores ingresados
            matriz_temp = []

            for i, fila_entradas in enumerate(self.entradas):
                fila_valores = []
                for j, entrada in enumerate(fila_entradas):
                    valor_texto = entrada.text()
                    if valor_texto.strip() == "":
                        raise ValueError(f"El campo {i+1},{j+1} está vacío.")

                    # Convertir el valor de texto a float y guardarlo en la fila temporal
                    valor = float(valor_texto)
                    fila_valores.append(valor)

                # Añadir la fila completa a la matriz temporal
                matriz_temp.append(fila_valores)

            self.matriz.matriz = matriz_temp
            # Añadir el QTextEdit con las expresiones al layout principal
            self.main_layout.addWidget(self.placeholder_respuestas)

            # Mostrar un mensaje indicando que la matriz ha sido almacenada correctamente
            QMessageBox.information(self, "Éxito", "Los valores de la matriz han sido guardados correctamente.")

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

    def agregar_vector(self):
        par_layout = QHBoxLayout()

        escalar_input = QLineEdit()
        escalar_input.setPlaceholderText("Escalar (para combinación)")
        self.escalar_inputs.append(escalar_input)
        par_layout.addWidget(escalar_input)
        vector_input = QLineEdit()
        vector_input.setPlaceholderText("Vector (separado por comas)")
        self.vector_inputs.append(vector_input)
        par_layout.addWidget(vector_input)
        self.vector_layout.addLayout(par_layout)

    def eliminar_vector(self):
        if self.vector_inputs:
            vector_input = self.vector_inputs.pop()
            vector_input.deleteLater()
        
        if self.escalar_inputs:
            escalar_input = self.escalar_inputs.pop()
            escalar_input.deleteLater()

    def calcular_vector_columna(self):
        try:
            # Crear una lista para almacenar los vectores individuales
            vectores_individuales_a_escalar = []
            escalar_list = []

            for escalar_input in self.escalar_inputs:
                escalar_text = escalar_input.text()
                
                if escalar_text.strip() == "":
                    raise ValueError("Uno de los escalares está vacío.")                
                try:
                    escalar_list.append(float(escalar_text.strip()))
                except ValueError:
                    raise ValueError(f"Valor no válido para escalar: {escalar_text}")

            if len(escalar_list) != len(self.vector_inputs):
                raise ValueError("El número de escalares no coincide con el número de vectores.")

            for index, vector_input in enumerate(self.vector_inputs):
                vector_text = vector_input.text()
                if vector_text.strip() == "":
                    raise ValueError("Uno de los vectores está vacío.")
                
                vector_list = [float(x.strip()) for x in vector_text.split(",")]
                
                # Aqui se instancias los vectores
                vector = Vector(len(vector_list), vector_list, orientacion="vertical")
                vectores_individuales_a_escalar.append(vector)  # Guardar cada vector individual

            self.lista_vectores_individuales = [vector_escalado.escalar_vector(escalar_list[index]) for vector_escalado in vectores_individuales_a_escalar]
            
            self.vector_columna, pasos = Vector.sumar_vectores(*self.lista_vectores_individuales)

            self.mostrar_resultados(pasos)

        except ValueError as e:
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
            # Verificar si la matriz y los vectores están ingresados correctamente
            if not hasattr(self, 'matriz') or not hasattr(self, 'lista_vectores_individuales'):
                raise ValueError("Debe ingresar la matriz y al menos un vector antes de realizar la multiplicación.")

            if len(self.matriz.matriz[0]) != self.vector_columna.dimension:
                    raise ValueError(f"El número de columnas de la matriz no coincide con la longitud del vector.")

            resultado_final, pasos_final = self.matriz.multiplicar_matriz_por_vector(self.vector_columna)

            # Crear el mensaje de resultado y pasos
            resultado_texto = f"Resultado de la multiplicación matriz por vector calculado: {resultado_final}\n\n"
            pasos_texto = "Pasos detallados de la multiplicación:\n"
            pasos_texto += pasos_final

            # Mostrar resultado y pasos usando la función mostrar_resultados
            self.mostrar_resultados(resultado_texto + pasos_texto)

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
            
    def realizar_multiplicacion_con_demostracion_distributiva(self):
        """Realiza la demostración completa de la propiedad distributiva con pasos detallados."""
        try:
            # Verificar si la matriz y los vectores están ingresados correctamente
            if not hasattr(self, 'matriz') or not hasattr(self, 'lista_vectores_individuales'):
                raise ValueError("Debe ingresar la matriz y al menos un vector antes de realizar la multiplicación.")

            # Crear una lista para almacenar los resultados de la multiplicación por cada vector
            resultados_individuales = []
            pasos_totales = "Demostración de la Propiedad Distributiva:\n\n"

            # Multiplicar la matriz por cada vector individual
            for idx, vector in enumerate(self.lista_vectores_individuales):
                # Verificar dimensiones antes de la multiplicación
                if len(self.matriz.matriz[0]) != vector.dimension:
                    raise ValueError(f"El número de columnas de la matriz no coincide con la longitud del vector {idx + 1}.")

                # Multiplicar la matriz por el vector individual y almacenar el resultado y pasos
                resultado_individual, pasos = self.matriz.multiplicar_matriz_por_vector(vector)
                resultados_individuales.append(resultado_individual)
                pasos_totales += f"Multiplicación de la matriz por el vector {idx + 1}:\n{pasos}\n\n"

            # Sumar los resultados individuales para obtener el vector columna final
            suma_resultado = [sum(fila) for fila in zip(*resultados_individuales)]
            pasos_totales += f"Sumando los resultados de cada vector:\n"

            # Mostrar cada suma por componente
            for i in range(len(suma_resultado)):
                componentes = [resultados[i] for resultados in resultados_individuales]
                pasos_totales += f"Componente {i + 1}: " + " + ".join(map(str, componentes)) + f" = {suma_resultado[i]}\n"

            pasos_totales += f"\nResultado de la suma de los productos individuales:\n{suma_resultado}\n\n"

            # Calcular el producto de la matriz por el vector calculado (suma de vectores)
            vector_calculado = Vector(len(suma_resultado), suma_resultado)
            resultado_vector_calculado, pasos_vector_calculado = self.matriz.multiplicar_matriz_por_vector(vector_calculado)
            pasos_totales += "Multiplicación de la matriz por el vector calculado (suma de los vectores):\n"
            pasos_totales += f"{pasos_vector_calculado}\n"

            # Verificar si los resultados coinciden
            if resultado_vector_calculado == suma_resultado:
                pasos_totales += "\n¡Se cumple la propiedad distributiva! El resultado es el mismo.\n"
            else:
                pasos_totales += "\nNo se cumple la propiedad distributiva. Hay una discrepancia en los resultados.\n"

            # Mostrar los pasos usando la función mostrar_resultados
            self.mostrar_resultados(pasos_totales)

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
    def mostrar_resultados(self, texto):
            # Eliminar el widget de placeholder_respuestas si existe
            if self.placeholder_respuestas is not None:
                self.main_layout.removeWidget(self.placeholder_respuestas)
                self.placeholder_respuestas.deleteLater()  # Eliminar correctamente el widget
                self.placeholder_respuestas = None  # Asegurarse de que no se vuelva a referenciar

            # Eliminar el widget de resultados anterior si existe
            if self.resultado_texto is not None:
                self.main_layout.removeWidget(self.resultado_texto)
                self.resultado_texto.deleteLater()
                self.resultado_texto = None  # Asegurarse de que no se vuelva a referenciar

            # Construir la expresión de la matriz multiplicada por el vector calculado
            matriz_vector_texto = "Expresiones de las Operaciones:\n"
            matriz_vector_texto += "Matriz * (Vector Calculado) = \n"
            for fila in self.matriz.matriz:
                matriz_vector_texto += f"{fila} * {self.vector_columna.vector}\n"
            
            matriz_vector_texto += "\nMatriz * (Vector 1) + Matriz * (Vector 2) + ... =\n"
            
            # Agregar cada operación de matriz por vector individual
            for idx, vector in enumerate(self.lista_vectores_individuales):
                matriz_vector_texto += f"Matriz * (Vector {idx + 1}) = \n"
                for fila in self.matriz.matriz:
                    matriz_vector_texto += f"{fila} * {vector.vector}\n"
                matriz_vector_texto += "\n"

            # Mostrar la matriz, los vectores y la expresión en el QTextEdit
            self.placeholder_respuestas = QTextEdit()
            self.placeholder_respuestas.setReadOnly(True)
            self.placeholder_respuestas.setFontFamily("Courier New")
            self.placeholder_respuestas.setText(matriz_vector_texto)

            # Fijar el tamaño del QTextEdit para la matriz y el vector
            self.placeholder_respuestas.setFixedSize(400, 200)  # Ajusta el tamaño según necesites

            # Añadir el QTextEdit con las expresiones al layout principal
            self.main_layout.addWidget(self.placeholder_respuestas)

            # Crear un nuevo QTextEdit para mostrar el resultado de los pasos
            self.resultado_texto = QTextEdit()
            self.resultado_texto.setReadOnly(True)
            self.resultado_texto.setFontFamily("Courier New")
            self.resultado_texto.setText(texto)

            # Añadir el QTextEdit al layout principal
            self.main_layout.addWidget(self.resultado_texto)

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
        self.main_layout = QVBoxLayout()

        # Inputs para dimensiones de las matrices
        self.n1_input = QLineEdit()
        self.m1_input = QLineEdit()
        self.n2_input = QLineEdit()
        self.m2_input = QLineEdit()
        self.crear_layout_top(
            labels_inputs=[("Filas de la primera matriz:", self.n1_input), ("Columnas de la primera matriz:", self.m1_input), ("Filas de la segunda matriz:", self.n2_input), ("Columnas de la segunda matriz:", self.m2_input)],
            boton_texto="Ingresar Dimensiones",
            boton_callback=self.configurar_matrices
        )

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

        # Botón para ejecutar la operación
        ejecutar_btn = QPushButton("Ejecutar Multiplicación de Matrices")
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

        # Botón para ingresar las dimensiones de las matrices
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

    def configurar_matrices(self):
        try:
            filas1 = int(self.n1_input.text())
            columnas1 = int(self.m1_input.text())
            filas2 = int(self.n2_input.text())
            columnas2 = int(self.m2_input.text())
            if filas1 <= 0 or columnas1 <= 0 or filas2 <= 0 or columnas2 <= 0:
                raise ValueError("Las dimensiones deben ser enteros positivos.")

            # Configurar el tamaño de las matrices
            self.filas1 = filas1
            self.columnas1 = columnas1
            self.filas2 = filas2
            self.columnas2 = columnas2

            # Limpiar matrices anteriores
            while self.inputs_layout.count():
                item = self.inputs_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # Agregar dos matrices con las dimensiones especificadas
            self.matriz_inputs = []
            for i, (f, c) in enumerate([(filas1, columnas1), (filas2, columnas2)]):
                layout = QVBoxLayout()
                titulo = QLabel(f"Matriz {i + 1}")
                layout.addWidget(titulo)

                grid_layout = QGridLayout()
                matriz_entradas = []
                for fila in range(f):
                    fila_entradas = []
                    for columna in range(c):
                        entrada = QLineEdit()
                        entrada.setPlaceholderText(f"({fila + 1}, {columna + 1})")
                        grid_layout.addWidget(entrada, fila, columna)
                        fila_entradas.append(entrada)
                    matriz_entradas.append(fila_entradas)

                layout.addLayout(grid_layout)
                self.inputs_layout.addLayout(layout)
                self.matriz_inputs.append(matriz_entradas)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

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
                            raise ValueError(f"El elemento ({i + 1},{j + 1}) de la matriz {idx + 1} está vacío.")
                        valor = float(valor_texto)
                        fila.append(valor)
                    matriz.append(fila)
                matriz_obj = Matriz(filas, columnas, matriz)
                matrices.append(matriz_obj)
            return matrices
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return []  # Retornar una lista vacía en caso de error

    def ejecutar_operacion(self):
        try:
            # Llamar a procesar_entrada_matrices para obtener la lista de objetos Matriz
            lista_matrices = self.procesar_entrada_matrices()
            if len(lista_matrices) != 2:
                return

            pasos = ""

            # Verificar si se deben transponer las matrices
            if self.transponer_matriz1_checkbox.isChecked():
                pasos += "Matriz 1 original: \n" + lista_matrices[0].mostrar() + " "
                lista_matrices[0] = Matriz.transponer_matriz(lista_matrices[0])
                pasos += "Matriz 1 transpuesta:\n" + lista_matrices[0].mostrar() + "\n"
            if self.transponer_matriz2_checkbox.isChecked():
                pasos += "Matriz 2 original: \n" + lista_matrices[1].mostrar() + " "
                lista_matrices[1] = Matriz.transponer_matriz(lista_matrices[1])
                pasos += "Matriz 2 transpuesta:\n" + lista_matrices[1].mostrar() + "\n"

            resultado, pasos_multiplicacion = lista_matrices[0].multiplicar_matrices(lista_matrices[1])
            pasos += pasos_multiplicacion

            # Verificar si se debe transponer el resultado
            if self.transponer_resultado_checkbox.isChecked():
                resultado = Matriz.transponer_matriz(resultado)
                pasos += "\nResultado transpuesto:\n" + resultado.mostrar()

            # Mostrar el resultado de la multiplicación de matrices
            self.resultado_texto.setText(pasos)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
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

# Iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())