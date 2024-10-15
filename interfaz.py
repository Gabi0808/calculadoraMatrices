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
    def configurar_grid_layout(n, m, aceptar_callback, nombre_boton = "Aceptar"):
 
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

        escalar_input_layout = QHBoxLayout()
        label = QLabel("Escalar del vector:")
        escalar_line_edit = QLineEdit()
        escalar_input_layout.addWidget(label)
        escalar_input_layout.addWidget(escalar_line_edit)
        entrada_escalar = [(label, escalar_line_edit)]

        # Usar QGridLayout para las entradas del vector
        grid_layout = QGridLayout()
        entradas_vector = []

        for i in range(dimension):
            etiqueta = QLabel(f"Componente {i + 1}:")
            entrada = QLineEdit()
            entrada.setPlaceholderText(f"Valor {i + 1}")

            if orientacion == "vertical":
                grid_layout.addWidget(etiqueta, i, 0)
                grid_layout.addWidget(entrada, i, 1)
            elif orientacion == "horizontal":
                grid_layout.addWidget(etiqueta, 0, i * 2)
                grid_layout.addWidget(entrada, 0, i * 2 + 1)
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

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        self.dimension_input = QLineEdit()
        self.vector_inputs = []
        self.escalar_inputs = []
        self.resultado_texto = None

        contenedor_layout, self.contenedor_vectores_layout, self.contenedor_botones_layout = InterfazHelper.crear_layout_vectores(
            n_input=self.dimension_input,
            ingresar_dimension_callback=self.ingresar_vectores
        )

        self.main_layout.addLayout(contenedor_layout)
                
    def ingresar_vectores(self):
       
        n = InterfazHelper.leer_entrada_dimension_vector(self.dimension_input)

        if n is None:
            return  

        InterfazHelper.crear_botones_vectores(lambda: InterfazHelper.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout, n),
                                              lambda: InterfazHelper.eliminar_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout),
                                              lambda: self.ejecutar_operacion(), 
                                              self.contenedor_botones_layout  
                                              )

        InterfazHelper.limpiar_entradas_vectores(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout)

        InterfazHelper.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout,n)
        InterfazHelper.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout,n)
   
    def procesar_entrada_vectores(self):
        try:
            
            valores_vector = [elemento for elemento in self.vector_inputs]        
            valores_escalar = [entrada[0][1] for entrada in self.escalar_inputs]

            lista_vectores_escalados = InterfazHelper.procesar_entrada(valores_vector, valores_escalar)

            return lista_vectores_escalados

        except ValueError as e:
            QMessageBox.critical(self, "Error al procesar entradas", str(e))
            return []

    def ejecutar_operacion(self):
        try:
            lista_vectores = self.procesar_entrada_vectores()
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
            ingresar_dimension_callback=self.ingresar_vectores
        )

        self.main_layout.addLayout(contenedor_layout)

    def ingresar_vectores(self):
            
        n = InterfazHelper.leer_entrada_dimension_vector(self.dimension_input)

        if n is None:
                return

        InterfazHelper.agregar_campo_vector(self.vector_fila_inputs, self.escalares_inputs, self.contenedor_vectores_layout, n, orientacion="horizontal")
        InterfazHelper.agregar_campo_vector(self.vector_columna_inputs, self.escalares_inputs, self.contenedor_vectores_layout, n, orientacion="vertical")
    
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
                boton_callback=lambda: self.ingresar_matriz()
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
        self.placeholder_respuestas = None
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

    def ingresar_matriz(self):
        try:
            
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            InterfazHelper.limpiar_grid_layout(self.grid_layout, self.contenedor_matriz)
            
            n, m = InterfazHelper.leer_entradas_dimensiones_matrices(self.n_input, self.m_input, self.rectangular)
            
            self.matriz = Matriz(n,m)
            
            self.grid_layout, self.entradas=InterfazHelper.configurar_grid_layout(n, m, self.guardar_matriz, nombre_boton="Guardar matriz")
        
            self.contenedor_matriz.addLayout(self.grid_layout)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")

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

class DeterminanteDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Ingresar Matriz")
        
        # Layout principal vertical
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        self.entradas = []
        self.grid_layout = None
        self.resultado_texto = None
        self.placeholder_respuestas = None
        self.matriz = None
        
        # Inputs para dimensiones de la matriz
        self.n_input = QLineEdit()
        self.m_input = self.n_input
         
        layout_dimensiones_matriz = InterfazHelper.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Dimensiones de la matriz:", self.n_input)],
            boton_texto="Ingresar Matriz",
            boton_callback=lambda: self.ingresar_matriz()
         )
        

        self.main_layout.addLayout(layout_dimensiones_matriz)
         
    def ingresar_matriz(self):
        try:
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            InterfazHelper.limpiar_grid_layout(self.grid_layout, self.main_layout)
            
            n, m = InterfazHelper.leer_entradas_dimensiones_matrices(self.n_input, self.m_input, rectangular=True)
            
            self.matriz = Matriz(n, m)
            
            self.grid_layout, self.entradas = InterfazHelper.configurar_grid_layout(n, m, self.calcular_determinante, nombre_boton="Calcular determinante")
        
            self.main_layout.addLayout(self.grid_layout)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")
        
    
    def calcular_determinante(self):
        try:
            self.matriz.matriz = InterfazHelper.procesar_entradas_matrices(self.entradas)
            
            # Calcular el determinante
            det = self.matriz.calcular_determinante()
            
            InterfazHelper.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            # Mostrar el determinante en la interfaz
            self.resultado_texto = InterfazHelper.mostrar_resultados(
                f"Determinante:\n{det}"
            )
            self.main_layout.addWidget(self.resultado_texto)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

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

# Iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())