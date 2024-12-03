import sys
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTextEdit, QWidget, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matrices import Matriz
from interfazHelper import InterfazHelperMatriz, InterfazHelperVector
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from utilidades import Formateador
from TransformCanvas import TransformCanvas

from PyQt5.QtWidgets import (
    QWidget, QSplitter, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt

class IngresarMatrizDialog(QWidget):
    def __init__(self, rectangular=False):
        super().__init__()
        self.rectangular = rectangular
        self.setGeometry(100, 100, 800, 600)  # Ancho más grande para acomodar el splitter
        self.setWindowTitle("Ingresar Matriz")

        # Splitter para dividir entradas y resultados
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.setContentsMargins(0, 0, 0, 0)

        # Layout izquierdo (entradas)
        self.input_widget = QWidget()
        self.input_layout = QVBoxLayout(self.input_widget)
        self.input_layout.setContentsMargins(20, 20, 20, 20)
        self.input_layout.setSpacing(10)
        self.input_layout.setAlignment(Qt.AlignTop)

        self.entradas = []
        self.grid_layout = None
        self.matriz = None

        self.n_input = QLineEdit()
        self.n_input.setPlaceholderText("Número de filas")

        self.m_input = QLineEdit()
        self.m_input.setPlaceholderText("Número de columnas")

        # Layout de dimensiones de la matriz
        if self.rectangular:
            layout_dimensiones_matriz = InterfazHelperMatriz.crear_layout_ingresar_dimensiones(
                labels_inputs=[("Filas de la matriz:", self.n_input), ("Columnas de la matriz:", self.m_input)],
                boton_texto="Ingresar Matriz",
                boton_callback=lambda: InterfazHelperMatriz.ingresar_matriz(
                    instancia=self,
                    main_layout=self.input_layout,
                    resultado_texto=self.resultado_texto,
                    grid_layout=self.grid_layout,
                    n_input=self.n_input,
                    m_input=self.m_input,
                    calcular_callback=self.resolver_gauss,
                    nombre_boton="Resolver Matriz por Gauss-Jordan",
                    target_layout=self.input_layout,
                    rectangular=True
                )
            )
        else:
            layout_dimensiones_matriz = InterfazHelperMatriz.crear_layout_ingresar_dimensiones(
                labels_inputs=[("Dimensiones de la matriz:", self.n_input)],
                boton_texto="Ingresar Matriz",
                boton_callback=lambda: InterfazHelperMatriz.ingresar_matriz(
                    instancia=self,
                    main_layout=self.input_layout,
                    resultado_texto=self.resultado_texto,
                    grid_layout=self.grid_layout,
                    n_input=self.n_input,
                    m_input=None,
                    calcular_callback=self.resolver_gauss,
                    nombre_boton="Resolver Matriz por Gauss-Jordan",
                    target_layout=self.input_layout,
                    rectangular=False
                )
            )

        self.input_layout.addLayout(layout_dimensiones_matriz)

        # Widget de resultados (derecho)
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_layout.setContentsMargins(20, 20, 20, 20)

        self.resultado_texto = None
        

        # Agregar widgets al splitter
        self.splitter.addWidget(self.input_widget)
        self.splitter.addWidget(self.result_widget)
        self.splitter.setSizes([350, 400])  # Tamaño inicial de las divisiones

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.splitter)

    def resolver_gauss(self):
        try:
            InterfazHelperMatriz.limpiar_resultados_texto(self.resultado_texto, self.result_layout)
            self.matriz.matriz = InterfazHelperMatriz.procesar_entradas_matrices(self.entradas)
            resultado, pasos = self.matriz.eliminacion_gauss_jordan()

            self.resultado_texto= InterfazHelperMatriz.mostrar_resultados(
                f"Soluciones:\n{self.matriz.calcular_soluciones_general()}\n\nResultado:\n{self.matriz.mostrar()}", 
                f"Pasos:\n{pasos}"
            )
            
            self.result_layout.addWidget(self.resultado_texto)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")
            
class MultiplicacionMatrizVectorDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)  # Aumentar tamaño de la ventana para más espacio
        self.setWindowTitle("Multiplicación de Matriz por Vector")

        # Layout principal vertical
        self.main_layout = QVBoxLayout(self)
        #self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Splitter para dividir entradas y resultados
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.setContentsMargins(0, 0, 0, 0)

        self.contenedor_izquierdo_widgets = QWidget()
        self.contenedor_izquierdo = QVBoxLayout(self.contenedor_izquierdo_widgets)
        self.contenedor_izquierdo.setAlignment(Qt.AlignTop)

        self.resultados_widget = QWidget()
        self.contenedor_resultados = QVBoxLayout(self.resultados_widget)
        self.contenedor_resultados.setAlignment(Qt.AlignTop)

        self.resultado_opcion = None

        #Nivel 1
        self.contenedor_inputs = QHBoxLayout()
        self.contenedor_matriz = QVBoxLayout()
        self.contenedor_vector = QHBoxLayout()
        self.contenedor_inputs.addLayout(self.contenedor_matriz)
        self.contenedor_inputs.addLayout(self.contenedor_vector)
        self.contenedor_izquierdo.addLayout(self.contenedor_inputs)
        
        #Nivel 2
        self.n_input = QLineEdit()
        self.m_input = QLineEdit()

        layout_dimensiones_matriz = InterfazHelperMatriz.crear_layout_ingresar_dimensiones(
                labels_inputs=[("Filas de la matriz:", self.n_input), ("Columnas de la matriz:", self.m_input)],
                boton_texto="Ingresar Matriz",
                boton_callback=lambda: InterfazHelperMatriz.ingresar_matriz(instancia=self,
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

        contenedor_layout, self.contenedor_vectores_layout, self.contenedor_botones_layout = InterfazHelperVector.crear_layout_vectores(
            n_input=self.dimension_vectores_input,
            ingresar_dimension_callback=self.ingresar_vectores
        )
        self.contenedor_vector.addLayout(contenedor_layout)

        # Matriz y vector que se multiplicaran al final
        self.matriz = None
        self.vector_columna = None
        self.resultado_texto = None
        self.grid_layout = None
        self.rectangular = True
        self.entradas = []
        self.calc_botones_layout = QHBoxLayout()
        self.vector_inputs = []
        self.escalar_inputs = []
        self.opciones_calc_combo_box = QComboBox()
        self.opciones_calc_combo_box.addItems(["","Calcular multiplicacion", "Visualizar transformacion"])
        self.transformCanvasWidget = None

        # Añadir el botón de calcular al final del main_layout
        calcular_btn = QPushButton("Calcular")
        calcular_btn.clicked.connect(self.calc_respuesta)
        self.calc_botones_layout.addWidget(calcular_btn)
        self.calc_botones_layout.addWidget(self.opciones_calc_combo_box)
        self.contenedor_izquierdo.addLayout(self.calc_botones_layout)

        self.splitter.addWidget(self.contenedor_izquierdo_widgets)
        self.splitter.addWidget(self.resultados_widget)
        self.splitter.setSizes([350, 100])
        self.main_layout.addWidget(self.splitter)

    def ingresar_vectores(self):
       
        n = InterfazHelperVector.leer_entrada_dimension_vector(self.dimension_vectores_input)

        if n is None:
            return  
        
        InterfazHelperVector.limpiar_entradas_vectores(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout)

        InterfazHelperVector.agregar_campo_vector(self.vector_inputs, self.escalar_inputs, self.contenedor_vectores_layout,n)

    def guardar_matriz(self):
        try:
            
            self.matriz.matriz = InterfazHelperMatriz.procesar_entradas_matrices(self.entradas)
            
            QMessageBox.information(self, "Éxito", "Los valores de la matriz han sido guardados correctamente.")

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

    def calc_respuesta(self):
        try:
            valores_vector_columna = InterfazHelperVector.procesar_entrada(self.vector_inputs, self.escalar_inputs)
            self.vector_columna = valores_vector_columna[0]
            opcion_seleccionada = self.opciones_calc_combo_box.currentText()
            
            if opcion_seleccionada == "Calcular multiplicacion":
                self.realizar_multiplicacion_matriz_vector()

            elif opcion_seleccionada == "Visualizar transformacion":
                if not hasattr(self, 'matriz') or not hasattr(self, 'vector_columna'):
                    raise ValueError("La matriz y el vector deben estar correctamente definidos antes de visualizar la transformación.")

                InterfazHelperMatriz.limpiar_resultados_texto(self.resultado_texto, self.contenedor_resultados)
                while self.contenedor_resultados.count() > 0:
                    widget = self.contenedor_resultados.takeAt(0).widget()
                    if widget is not None:
                        widget.deleteLater()

                #self.visualizador = VisualizadorMatrizPorVector(self.matriz, self.vector_columna)
                resultado_final, _ = self.matriz.multiplicar_matriz_por_vector(self.vector_columna)
                self.transformCanvasWidget = TransformCanvas(self.matriz, self.vector_columna, self)
                html = Formateador.box_matrix_and_vectors(
                    self.matriz.matriz,  # Asegúrate de que devuelve una lista de listas
                    self.vector_columna.vector,  # Lista de números
                    resultado_final.vector  # Lista de números
                )

                self.transformCanvasWidget.datos.setHtml(html)

                self.contenedor_resultados.addWidget(self.transformCanvasWidget.get_widget())
            else:
                print("Ingrese una opción válida")        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al ejecutar la operación: {str(e)}")

    def realizar_multiplicacion_matriz_vector(self):
        try:

            if not hasattr(self, 'matriz') or not self.vector_columna:
                raise ValueError("Debe ingresar la matriz y calcular el vector antes de realizar la multiplicación.")

            if len(self.matriz.matriz[0]) != len(self.vector_columna.vector):
                raise ValueError("El número de columnas de la matriz debe coincidir con la longitud del vector.")

            resultado_final, pasos_final = self.matriz.multiplicar_matriz_por_vector(self.vector_columna)

            while self.contenedor_resultados.count() > 0:
                    widget = self.contenedor_resultados.takeAt(0).widget()
                    if widget is not None:
                        widget.deleteLater()

            InterfazHelperMatriz.limpiar_resultados_texto(self.resultado_opcion, self.contenedor_resultados)
            self.resultado_texto = InterfazHelperMatriz.mostrar_resultados(f"Resultado de la multiplicación de matriz por vector:\n{Formateador.box_vector(resultado_final.vector)}",
                                                                           f"Pasos detallados de la multiplicación:\n\n {pasos_final}")
            self.contenedor_resultados.addWidget(self.resultado_texto)

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

class OperacionesMatrizDialog(QWidget):
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
    
class MultiplicacionMatricesDialog(QWidget):
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

        layout_dimensiones_matriz_1 = InterfazHelperMatriz.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Filas de la Matriz 1:", self.n_inputs[0]),("Columnas de la Matriz 1:", self.m_inputs[0]), 
                           ("Filas de la Matriz 2:", self.n_inputs[1]),("Columnas de la Matriz 2:", self.m_inputs[1])],
            boton_texto="Ingresar Matrices",
            boton_callback=lambda: InterfazHelperMatriz.ingresar_multiples_matrices(instancia=self,
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
                matriz.matriz = InterfazHelperMatriz.procesar_entradas_matrices(self.entradas_matrices[indx])
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


            InterfazHelperMatriz.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            self.resultado_texto = InterfazHelperMatriz.mostrar_resultados(f"Resultado de la multiplicacion de Matrices:\n\n{resultado.mostrar} ",
                                                                           f"Pasos de la multiplicacion de matrices:\n\n{pasos}")

            self.main_layout.addWidget(self.resultado_texto)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class TranspuestaDialog(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 600, 400)  # Tamaño inicial ajustado
        self.setWindowTitle("Transposición de Matriz")
        
        self.splitter = QSplitter(Qt.Horizontal, self)
        
        self.entrada_widget = QWidget()
        self.entrada_layout = QVBoxLayout(self.entrada_widget)
        self.entrada_layout.setContentsMargins(20, 20, 20, 20)
        self.entrada_layout.setSpacing(10)
        self.entrada_layout.setAlignment(Qt.AlignTop)
        
        self.entradas = []
        self.grid_layout = None
        self.matriz = None
        self.n_input = QLineEdit()
        self.m_input = self.n_input
        
        layout_dimensiones_matriz = InterfazHelperMatriz.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Dimensiones de la matriz:", self.n_input)],
            boton_texto="Ingresar Matriz",
            boton_callback=lambda: InterfazHelperMatriz.ingresar_matriz(
                instancia=self,
                main_layout=self.entrada_layout,
                resultado_texto=None,
                grid_layout=self.grid_layout,
                n_input=self.n_input,
                m_input=self.m_input,
                calcular_callback=self.calcular_transpuesta,
                nombre_boton="Calcular Transpuesta",
                rectangular=True,
                target_layout=self.entrada_layout
            )
        )
        self.entrada_layout.addLayout(layout_dimensiones_matriz)
        
        # Lado derecho: Contenedor de resultados
        self.resultado_widget = QWidget()
        self.resultado_layout = QVBoxLayout(self.resultado_widget)
        self.resultado_layout.setContentsMargins(20, 20, 20, 20)
        self.resultado_layout.setSpacing(10)
        self.resultado_layout.setAlignment(Qt.AlignTop)
        
        # Añadir widgets al splitter
        self.splitter.addWidget(self.entrada_widget)
        self.splitter.addWidget(self.resultado_widget)
        self.splitter.setSizes([300, 300])  # Configurar tamaños iniciales

        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.splitter)
    
    def calcular_transpuesta(self):
        try:
            self.matriz.matriz = InterfazHelperMatriz.procesar_entradas_matrices(self.entradas)
            
            matriz_transpuesta = Matriz.transponer_matriz(self.matriz)
            
            while self.resultado_layout.count() > 0:
                widget = self.resultado_layout.takeAt(0).widget()
                if widget is not None:
                    widget.deleteLater()
            
            resultado_texto = InterfazHelperMatriz.mostrar_resultados(f"Matriz Transpuesta:\n{matriz_transpuesta.mostrar()}",
                                                                      f"Matriz original:\n{self.matriz.mostrar()}\n\nMatriz Transpuesta:\n{matriz_transpuesta.mostrar()}"
            )
            self.resultado_layout.addWidget(resultado_texto)
        
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

class DeterminanteDialog(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 600, 400)  # Tamaño ajustado
        self.setWindowTitle("Cálculo del Determinante")
        
        # Crear un QSplitter para dividir la ventana en dos partes
        self.splitter = QSplitter(Qt.Horizontal, self)
        
        # Lado izquierdo: Contenedor de entrada
        self.entrada_widget = QWidget()
        self.entrada_layout = QVBoxLayout(self.entrada_widget)
        self.entrada_layout.setContentsMargins(20, 20, 20, 20)
        self.entrada_layout.setSpacing(10)
        self.entrada_layout.setAlignment(Qt.AlignTop)
        
        # Configuración de entradas
        self.entradas = []
        self.grid_layout = None
        self.matriz = None
        self.resultado_texto = None
        self.n_input = QLineEdit()
        self.m_input = self.n_input
        
        # Layout para ingresar dimensiones de la matriz
        layout_dimensiones_matriz = InterfazHelperMatriz.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Dimensiones de la matriz:", self.n_input)],
            boton_texto="Ingresar Matriz",
            boton_callback=lambda: InterfazHelperMatriz.ingresar_matriz(
                instancia=self,
                main_layout=self.entrada_layout,
                resultado_texto=None,
                grid_layout=self.grid_layout,
                n_input=self.n_input,
                m_input=self.m_input,
                calcular_callback=self.calcular_determinante,
                nombre_boton="Calcular determinante",
                rectangular=True,
                target_layout=self.entrada_layout
            )
        )
        self.entrada_layout.addLayout(layout_dimensiones_matriz)
        
        # Lado derecho: Contenedor de resultados
        self.resultado_widget = QWidget()
        self.resultado_layout = QVBoxLayout(self.resultado_widget)
        self.resultado_layout.setContentsMargins(20, 20, 20, 20)
        self.resultado_layout.setSpacing(10)
        self.resultado_layout.setAlignment(Qt.AlignTop)
        
        # Añadir widgets al splitter
        self.splitter.addWidget(self.entrada_widget)
        self.splitter.addWidget(self.resultado_widget)
        self.splitter.setSizes([300, 300])  # Configurar tamaños iniciales

        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.splitter)
    
    def calcular_determinante(self):
        try:
            self.matriz.matriz = InterfazHelperMatriz.procesar_entradas_matrices(self.entradas)
            
            det, pasos = self.matriz.calcular_determinante()
            
            InterfazHelperMatriz.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            self.resultado_texto = InterfazHelperMatriz.mostrar_resultados(
                f"Determinante:\n{det}",
                f"Pasos:\n{pasos}"
            )
    
            self.resultado_layout.addWidget(self.resultado_texto)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al ingresar datos: {str(e)}")

class CramerDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resolver Sistema por Regla de Cramer")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        # Crear un QSplitter para dividir la ventana en dos partes
        self.splitter = QSplitter(Qt.Horizontal, self)

        # Lado izquierdo: Configuración de matriz y vector
        self.entrada_widget = QWidget()
        self.entrada_layout = QVBoxLayout(self.entrada_widget)
        self.entrada_layout.setContentsMargins(20, 20, 20, 20)
        self.entrada_layout.setSpacing(10)
        self.entrada_layout.setAlignment(Qt.AlignTop)

        self.n_input = QLineEdit()
        self.n_input.setPlaceholderText("Número de ecuaciones (n)")
        self.grid_layout = None

        layout_dimensiones = InterfazHelperMatriz.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Número de ecuaciones:", self.n_input)],
            boton_texto="Configurar Matriz",
            boton_callback=lambda: InterfazHelperMatriz.configurar_matriz_y_vector(
                instancia=self,
                main_layout=self.entrada_layout,
                resultado_texto=None,
                grid_layout=self.grid_layout,
                n_input=self.n_input,
                calcular_callback=self.calcular_cramer,
                nombre_boton="Calcular por regla de Cramer",
                target_layout=self.entrada_layout,
            )
        )
        self.entrada_layout.addLayout(layout_dimensiones)

        self.entradas_matriz = []
        self.entradas_vector = []

        # Lado derecho: Resultados
        self.resultado_widget = QWidget()
        self.resultado_layout = QVBoxLayout(self.resultado_widget)
        self.resultado_layout.setContentsMargins(20, 20, 20, 20)
        self.resultado_layout.setSpacing(10)
        self.resultado_layout.setAlignment(Qt.AlignTop)

        # Añadir widgets al splitter
        self.splitter.addWidget(self.entrada_widget)
        self.splitter.addWidget(self.resultado_widget)
        self.splitter.setSizes([300, 300])  # Configurar tamaños iniciales

        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.splitter)

        self.resultado_texto = None

    def calcular_cramer(self):
        try:
        
            matriz_valores = InterfazHelperMatriz.procesar_entradas_matrices(self.entradas_matriz)
            vector_constantes = [float(entrada.text()) for entrada in self.entradas_vector]

            matriz = Matriz(len(matriz_valores), len(matriz_valores), matriz_valores)
            soluciones, mensaje_o_pasos = matriz.resolver_cramer(vector_constantes)
            
            if soluciones is None:
                QMessageBox.warning(self, "Sin solución", mensaje_o_pasos)
            else:
                texto_resultado = "\n".join([f"x{i+1} = {sol}" for i, sol in enumerate(map(str, soluciones))])

                InterfazHelperMatriz.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
                resultado_texto_widget = InterfazHelperMatriz.mostrar_resultados(f"Soluciones:\n{texto_resultado}",
                                                                                 f"Pasos:\n{mensaje_o_pasos}")
                
                self.resultado_layout.addWidget(resultado_texto_widget)
                self.resultado_texto = resultado_texto_widget

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

class InversaTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cálculo de Matriz Inversa")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        # Crear un QSplitter para dividir la ventana en dos partes
        self.splitter = QSplitter(Qt.Horizontal, self)

        # Lado izquierdo: Configuración de la matriz
        self.entrada_widget = QWidget()
        self.entrada_layout = QVBoxLayout(self.entrada_widget)
        self.entrada_layout.setContentsMargins(20, 20, 20, 20)
        self.entrada_layout.setSpacing(10)
        self.entrada_layout.setAlignment(Qt.AlignTop)

        self.entradas = []
        self.grid_layout = None
        self.resultado_texto = None
        self.matriz = None

        self.n_input = QLineEdit()
        self.n_input.setPlaceholderText("Dimensiones de la matriz (n x n)")
        self.m_input = self.n_input

        layout_dimensiones_matriz = InterfazHelperMatriz.crear_layout_ingresar_dimensiones(
            labels_inputs=[("Dimensiones de la matriz:", self.n_input)],
            boton_texto="Ingresar Matriz",
            boton_callback=lambda: InterfazHelperMatriz.ingresar_matriz(
                instancia=self,
                main_layout=self.entrada_layout,
                resultado_texto=None,
                grid_layout=self.grid_layout, 
                n_input=self.n_input, 
                m_input=self.m_input,
                calcular_callback=self.calcular_inversa, 
                nombre_boton="Calcular matriz Inversa",
                target_layout=self.entrada_layout,
            )
        )
        
        self.entrada_layout.addLayout(layout_dimensiones_matriz)

        # Lado derecho: Resultados
        self.resultado_widget = QWidget()
        self.resultado_layout = QVBoxLayout(self.resultado_widget)
        self.resultado_layout.setContentsMargins(20, 20, 20, 20)
        self.resultado_layout.setSpacing(10)
        self.resultado_layout.setAlignment(Qt.AlignTop)

        # Añadir widgets al splitter
        self.splitter.addWidget(self.entrada_widget)
        self.splitter.addWidget(self.resultado_widget)
        self.splitter.setSizes([300, 300])  # Configurar tamaños iniciales

        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.splitter)

         
    def calcular_inversa(self):
        try:
            self.matriz.matriz = InterfazHelperMatriz.procesar_entradas_matrices(self.entradas)
            matriz_inversa, pasos = self.matriz.calcular_inversa()
            
            InterfazHelperMatriz.limpiar_resultados_texto(self.resultado_texto, self.main_layout)
            
            self.resultado_texto = InterfazHelperMatriz.mostrar_resultados(
                f"Matriz inversa:\n{matriz_inversa.mostrar()}",
                f"Pasos:\n{pasos}"
            )
            
            self.resultado_layout.addWidget(self.resultado_texto)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"{str(e)}")
