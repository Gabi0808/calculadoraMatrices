import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSpacerItem, QSizePolicy, QMessageBox, QTextEdit, QMainWindow, QWidget, QComboBox,
)
from PyQt5.QtCore import Qt
from matrices import Matriz
from vectores import Vector
from utilidades import *

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

            vector_escalares = zip(vectores, escalares)

            # Crear la lista de vectores usando la clase Vector correctamente
            lista_vectores = [Vector(len(vector), vector, escalar) for vector, escalar in vector_escalares]
            return lista_vectores
        
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return []  # Retornar una lista vacía en caso de error
        
    def ejecutar_operacion(self):
            
        try:
            # Llamar a procesar_entrada_vectores para obtener la lista de objetos Vector
            lista_vectores = self.procesar_entrada_vectores()
            if not lista_vectores:
                return  # Salir si no se pudo procesar la entrada
            
            # Desempaquetar la lista de objetos Vector al pasarla a sumar_vectores
            resultado, pasos = Vector.sumar_vectores(*lista_vectores)
            
            # Mostrar los pasos y el resultado en el área de texto
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
            vector_fila_obj = Vector(len(vector_fila), vector_fila)
            vector_columna_obj = Vector(len(vector_columna), vector_columna)

            # Calcular el producto de vector fila por vector columna usando la nueva función
            resultado, pasos = vector_fila_obj.producto_vector_fila_por_vector_columna(vector_columna_obj)

            # Mostrar el resultado en la interfaz
            resultado_texto = f"{pasos}\nResultado del producto: {resultado}"
            self.resultado_texto.setText(resultado_texto)
            

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

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
        calcular_btn = QPushButton("Calcular Multiplicación")
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
            self.lista_vectores_individuales = []
            escalar_list = []

            for escalar_input in self.escalar_inputs:
                escalar_text = escalar_input.text()
                
                if escalar_text.strip() == "":
                    raise ValueError("Uno de los escalares está vacío.")                
                # Convertir el texto en un número flotante (si hay varios escalares separados por comas, tomará el primero)
                try:
                    escalar_list.append(float(escalar_text.strip()))
                except ValueError:
                    raise ValueError(f"Valor no válido para escalar: {escalar_text}")

            if len(escalar_list) != len(self.vector_inputs):
                raise ValueError("El número de escalares no coincide con el número de vectores.")

            # Recolectar los vectores y asociar el escalar correspondiente
            for index, vector_input in enumerate(self.vector_inputs):
                vector_text = vector_input.text()
                if vector_text.strip() == "":
                    raise ValueError("Uno de los vectores está vacío.")
                
                vector_list = [float(x.strip()) for x in vector_text.split(",")]
                
                # Aqui se instancias los vectores
                vector = Vector(len(vector_list), vector_list, escalar_list[index])
                self.lista_vectores_individuales.append(vector)  # Guardar cada vector individual

            vector_suma, pasos = Vector.sumar_vectores(*self.lista_vectores_individuales)

            # Crear un nuevo vector columna con el resultado de la suma
            self.vector_columna = Vector(len(vector_suma), vector_suma)

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
            else:
                print("Ingrese una opcion") 
                
        except:
            raise ValueError(f"No se ha seleccionado ninguna opcion valida")        
        

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
        
        # Añadir botón para la multiplicación de matriz por vector
        self.multiplicacion_matriz_vector_btn = QPushButton("Multiplicación de Matriz por Vector")
        self.multiplicacion_matriz_vector_btn.clicked.connect(self.mostrar_multiplicacion_matriz_vector_dialog)
        self.layout.addWidget(self.multiplicacion_matriz_vector_btn)
        
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

# Iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())