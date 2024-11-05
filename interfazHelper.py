from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTextEdit, QWidget, QLayout
)
from PyQt5.QtCore import Qt
from matrices import Matriz
from vectores import Vector
from visualizador import *

class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            event.accept()  
        else:
            super().keyPressEvent(event)

class InterfazHelperMatriz():
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
            InterfazHelperMatriz.limpiar_resultados_texto(resultado_texto, main_layout)
            InterfazHelperMatriz.limpiar_grid_layout(grid_layout, target_layout)

            # Leer dimensiones
            n, m = InterfazHelperMatriz.leer_entradas_dimensiones_matrices(n_input, m_input, rectangular=rectangular)

            nueva_matriz = Matriz(n, m)

            # Configurar nuevo grid_layout y asignarlo a la referencia actual
            nuevo_grid_layout, nuevas_entradas = InterfazHelperMatriz.configurar_grid_layout(n, m, calcular_callback, nombre_boton=nombre_boton)
            
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
            InterfazHelperMatriz.limpiar_resultados_texto(resultado_texto, main_layout)

            for item in grid_layouts:
                if isinstance(item, QLayout):
                    InterfazHelperMatriz.limpiar_grid_layout(item, target_layout)
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
                n, m = InterfazHelperMatriz.leer_entradas_dimensiones_matrices(n_inputs[i], m_inputs[i], rectangular=rectangular)
                nueva_matriz = Matriz(n, m)
                nuevas_matrices.append(nueva_matriz)

                nuevo_grid_layout, entradas = InterfazHelperMatriz.configurar_grid_layout(n, m, aceptar_callback=None, nombre_boton=None, inlcuir_boton=False)
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
        
        dimension_layout = InterfazHelperMatriz.crear_layout_ingresar_dimensiones(
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
        
        InterfazHelperMatriz.limpiar_botones_vectores(contenedor_layout)

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
        
        entrada_escalar, entrada_vector, contenedor_entradas_vector = InterfazHelperMatriz.crear_entrada_vector(n, orientacion)
        
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
            InterfazHelperMatriz.eliminar_vector(vector_inputs, escalar_inputs, inputs_layout) 

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

            InterfazHelperMatriz.limpiar_resultados_texto(resultado_texto, main_layout)
            InterfazHelperMatriz.limpiar_grid_layout(grid_layout, target_layout)

            layout_matriz_vector = QHBoxLayout()

            layout_matriz = QVBoxLayout()
            etiqueta_matriz = QLabel("Matriz")
            etiqueta_matriz.setAlignment(Qt.AlignCenter)
            layout_matriz.addWidget(etiqueta_matriz)

            grid_layout_matriz, entradas_matriz = InterfazHelperMatriz.configurar_grid_layout(n, n, aceptar_callback=None, nombre_boton=None, inlcuir_boton=False)
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
  
        n = InterfazHelperMatriz.leer_entrada_dimension_vector(dimension_input)

        if n is None:
            return

        InterfazHelperMatriz.crear_botones_vectores(
            lambda: InterfazHelperMatriz.agregar_campo_vector(vector_inputs, escalar_inputs, contenedor_vectores_layout, n, orientaciones[len(vector_inputs) % len(orientaciones)]),
            lambda: InterfazHelperMatriz.eliminar_vector(vector_inputs, escalar_inputs, contenedor_vectores_layout),
            ejecutar_callback,
            contenedor_botones_layout
        )

        InterfazHelperMatriz.limpiar_entradas_vectores(vector_inputs, escalar_inputs, contenedor_vectores_layout)

        for orientacion in orientaciones:
            InterfazHelperMatriz.agregar_campo_vector(vector_inputs, escalar_inputs, contenedor_vectores_layout, n, orientacion)

    @staticmethod
    def leer_entrada_vectores_escalares(vector_inputs, escalar_inputs):
        try:

            valores_vector = [elemento for elemento in vector_inputs]
            valores_escalar = [entrada[0][1] for entrada in escalar_inputs]

            lista_vectores_escalados = InterfazHelperMatriz.procesar_entrada(valores_vector, valores_escalar)

            return lista_vectores_escalados

        except ValueError as e:
            QMessageBox.critical(None, "Error al procesar entradas", str(e))
            return []

class InterfazHelperAnalisisNumerico():
    pass