from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSplitter,QMessageBox)
from PyQt5.QtCore import Qt
import sympy as sym
from analisisNumerico import Funcion
from interfazHelper import InterfazHelperAnalisisNumerico

class BiseccionTab(QWidget):
    def __init__(self):
        super().__init__()

        splitter = QSplitter(Qt.Horizontal)

        entradas_widget = QWidget()
        entradas_layout = QVBoxLayout(entradas_widget)
        entradas_layout.setAlignment(Qt.AlignTop)

        contenedor_funcion, self.input_funcion, self.latex_label = InterfazHelperAnalisisNumerico.crear_funcion_input_latex("Ingrese la función en términos de 'x':", self.actualizar_latex)
        
        contenedor_intervalos, self.input_a, self.input_b = InterfazHelperAnalisisNumerico.crear_intervalos_input("Ingrese el valor de 'a':","Ingrese el valor de 'b':")
        
        self.boton_calcular = InterfazHelperAnalisisNumerico.crear_boton("Calcular Bisección Múltiple", self.calcular_biseccion_multiple)
        self.boton_siguiente = InterfazHelperAnalisisNumerico.crear_boton("Siguiente Iteración", self.siguiente_iteracion)
        self.boton_siguiente.setEnabled(False)
        
        self.text_edit_resultado = InterfazHelperAnalisisNumerico.crear_text_edit()
        
        entradas_layout.addLayout(contenedor_funcion)

        entradas_layout.addLayout(contenedor_intervalos)
        
        entradas_layout.addWidget(self.boton_calcular)
        entradas_layout.addWidget(self.boton_siguiente)
        entradas_layout.addWidget(QLabel("Registro de iteraciones:"))
        entradas_layout.addWidget(self.text_edit_resultado)

        grafico_widget, self.canvas = InterfazHelperAnalisisNumerico.crear_canvas_widget(self)

        splitter.addWidget(entradas_widget)
        splitter.addWidget(grafico_widget)

        splitter.setSizes([900, 800])

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(splitter)

        self.iteraciones = []
        self.iteracion_actual = 0
        self.raiz_actual = 0
        self.raices = []
        self.registros = []
        self.puntos_por_raiz = []
        self.xlim = (-50, 50)
        self.ylim = (-50, 50)
        self.initial_xlim = (-5, 5)  
        self.initial_ylim = (-5, 5)

    def actualizar_latex(self):
        funcion_texto = self.input_funcion.text()
        try:
            self.funcion = Funcion(funcion_texto)
            latex_str = sym.latex(self.funcion.funcion)
            InterfazHelperAnalisisNumerico.mostrar_latex(latex_str, self.latex_label)
            self.graficar_funcion()  # Graficar la función automáticamente
        except Exception:
            self.latex_label.clear()

    def calcular_biseccion_multiple(self):
        try:
            funcion_texto = self.input_funcion.text()
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            self.funcion = Funcion(funcion_texto)
            self.raices, self.registros, self.puntos_por_raiz = self.funcion.biseccion_multiple(a, b, subintervalos=10, tolerancia=1e-6)
            self.raiz_actual = 0
            self.iteracion_actual = 0
            if self.raices:
                self.boton_siguiente.setEnabled(True)
                self.text_edit_resultado.setText(self.registros[0])

                # Pasar los valores de a, b, c de la primera iteración a actualizar_grafico
                a, b, c = self.puntos_por_raiz[self.raiz_actual][self.iteracion_actual]
                self.actualizar_grafico(a, b, c)
            else:
                QMessageBox.information(self, "Resultado", "No se encontraron raíces.")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada no válida: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def siguiente_iteracion(self):
        if self.iteracion_actual < len(self.puntos_por_raiz[self.raiz_actual]) - 1:
            self.iteracion_actual += 1
        else:
            if self.raiz_actual < len(self.raices) - 1:
                self.raiz_actual += 1
                self.iteracion_actual = 0
                self.text_edit_resultado.setText(self.registros[self.raiz_actual])
            else:
                QMessageBox.information(self, "Fin", "Todas las iteraciones han terminado.")
                self.boton_siguiente.setEnabled(False)
                return
        
        a, b, c = self.puntos_por_raiz[self.raiz_actual][self.iteracion_actual]
        self.actualizar_grafico(a, b, c)

    def graficar_funcion(self):

        for line in self.canvas.ax.get_lines():
            line.remove()

        x_min, x_max = self.xlim
        num_points = 1000
        x_vals = [x_min + i * (x_max - x_min) / (num_points - 1) for i in range(num_points)]
        
        # Evaluar la función en cada x
        y_vals = [self.funcion.evaluar_funcion(x) for x in x_vals]

        # Graficar la función
        self.canvas.ax.plot(x_vals, y_vals, label="f(x)", color='blue')
        self.canvas.ax.axhline(0, color='black', linewidth=0.5)
        self.canvas.ax.axvline(0, color='black', linewidth=0.5)
        self.canvas.ax.set_xlim(self.xlim)
        self.canvas.ax.set_ylim(self.ylim)
        self.canvas.ax.set_xlim(self.initial_xlim)
        self.canvas.ax.set_ylim(self.initial_ylim)
        self.canvas.ax.grid(True)
        self.canvas.ax.set_aspect('equal', adjustable='box')
        self.canvas.ax.legend()
        self.canvas.draw()

    def actualizar_grafico(self, a, b, c):
        if not hasattr(self, 'grafico_fijo'):
            self.graficar_funcion()
            self.grafico_fijo = True

        # Limpiar los puntos de la iteración anterior
        [p.remove() for p in getattr(self, 'puntos_iteracion', []) if p]
        self.puntos_iteracion = []

        # Graficar los puntos de a, b, y c de la iteración actual
        f_a = self.funcion.evaluar_funcion(a)
        f_b = self.funcion.evaluar_funcion(b)
        f_c = self.funcion.evaluar_funcion(c)

        if f_a is not None:
            self.puntos_iteracion.append(self.canvas.ax.plot(a, f_a, 'ro', label='a')[0])
        if f_b is not None:
            self.puntos_iteracion.append(self.canvas.ax.plot(b, f_b, 'yo', label='b')[0])
        if f_c is not None:
            self.puntos_iteracion.append(self.canvas.ax.plot(c, f_c, 'go', label='c')[0])

        self.canvas.ax.legend()
        self.canvas.draw()

class NewtonRaphsonTab(QWidget):
    def __init__(self):
        super().__init__()

        splitter = QSplitter(Qt.Horizontal)

        entradas_widget = QWidget()
        entradas_layout = QVBoxLayout(entradas_widget)
        entradas_layout.setAlignment(Qt.AlignTop)

        # Entrada de la función
        contenedor_funcion, self.input_funcion, self.latex_label = InterfazHelperAnalisisNumerico.crear_funcion_input_latex(texto="Ingrese la función en términos de 'x':",callback_actualizar_latex= self.actualizar_latex)
        
        contenedor_inicial = QVBoxLayout()  # Crear un layout o contenedor si es necesario
        self.input_x0 = InterfazHelperAnalisisNumerico.crear_input("Ingrese el valor inicial 'x0':")
        contenedor_inicial.addWidget(self.input_x0)

        # Botones
        self.boton_calcular = InterfazHelperAnalisisNumerico.crear_boton("Calcular Newton-Raphson", self.calcular_newton_raphson)
        self.boton_siguiente = InterfazHelperAnalisisNumerico.crear_boton("Siguiente Iteración", self.siguiente_iteracion)
        self.boton_siguiente.setEnabled(False)
        
        # Cuadro de texto para mostrar el registro
        self.text_edit_resultado = InterfazHelperAnalisisNumerico.crear_text_edit()
        
        # Añadir elementos al layout de entrada
        entradas_layout.addLayout(contenedor_funcion)
        entradas_layout.addLayout(contenedor_inicial)
        entradas_layout.addWidget(self.boton_calcular)
        entradas_layout.addWidget(self.boton_siguiente)
        entradas_layout.addWidget(QLabel("Registro de iteraciones:"))
        entradas_layout.addWidget(self.text_edit_resultado)

        # Widget para el gráfico
        grafico_widget, self.canvas = InterfazHelperAnalisisNumerico.crear_canvas_widget(self)

        # Añadir widgets al splitter
        splitter.addWidget(entradas_widget)
        splitter.addWidget(grafico_widget)

        # Ajustar tamaños de los elementos
        splitter.setSizes([900, 800])

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(splitter)

        # Variables de control para el método
        self.iteraciones = []
        self.iteracion_actual = 0
        self.x_actual = 0
        self.registro = ""

        # Rango inicial de visualización en el gráfico
        self.xlim = (-50, 50)
        self.ylim = (-50, 50)
        self.initial_xlim = (-5, 5)
        self.initial_ylim = (-5, 5)

    def actualizar_latex(self):
        funcion_texto = self.input_funcion.text()
        try:
            self.funcion = Funcion(funcion_texto)
            latex_str = sym.latex(self.funcion.funcion)
            InterfazHelperAnalisisNumerico.mostrar_latex(latex_str, self.latex_label)
            self.graficar_funcion()  # Graficar la función automáticamente
        except Exception:
            self.latex_label.clear()

    def calcular_newton_raphson(self):
        try:
            funcion_texto = self.input_funcion.text()
            x0 = float(self.input_x0.text())
            self.funcion = Funcion(funcion_texto)
            raiz, self.registro = self.funcion.newton_raphson(x0, tolerancia=1e-6)
            self.x_actual = x0
            self.iteracion_actual = 0

            if raiz is not None:
                self.boton_siguiente.setEnabled(True)
                self.text_edit_resultado.setText(self.registro)
                self.actualizar_grafico(self.x_actual)
            else:
                QMessageBox.information(self, "Resultado", "No se encontró una raíz con el método Newton-Raphson.")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada no válida: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def siguiente_iteracion(self):
        if self.iteracion_actual < len(self.iteraciones) - 1:
            self.iteracion_actual += 1
            self.x_actual = self.iteraciones[self.iteracion_actual]
            self.text_edit_resultado.setText(self.registro)
            self.actualizar_grafico(self.x_actual)
        else:
            QMessageBox.information(self, "Fin", "Todas las iteraciones han terminado.")
            self.boton_siguiente.setEnabled(False)

    def graficar_funcion(self):
        for line in self.canvas.ax.get_lines():
            line.remove()

        x_min, x_max = self.xlim
        num_points = 1000
        x_vals = [x_min + i * (x_max - x_min) / (num_points - 1) for i in range(num_points)]
        
        y_vals = [self.funcion.evaluar_funcion(x) for x in x_vals]

        self.canvas.ax.plot(x_vals, y_vals, label="f(x)", color='blue')
        self.canvas.ax.axhline(0, color='black', linewidth=0.5)
        self.canvas.ax.axvline(0, color='black', linewidth=0.5)
        self.canvas.ax.set_xlim(self.xlim)
        self.canvas.ax.set_ylim(self.ylim)
        self.canvas.ax.set_xlim(self.initial_xlim)
        self.canvas.ax.set_ylim(self.initial_ylim)
        self.canvas.ax.grid(True)
        self.canvas.ax.set_aspect('equal', adjustable='box')
        self.canvas.ax.legend()
        self.canvas.draw()

    def actualizar_grafico(self, x):
        if not hasattr(self, 'grafico_fijo'):
            self.graficar_funcion()
            self.grafico_fijo = True

        # Limpiar puntos de la iteración anterior
        [p.remove() for p in getattr(self, 'puntos_iteracion', []) if p]
        self.puntos_iteracion = []

        # Graficar el punto x de la iteración actual
        f_x = self.funcion.evaluar_funcion(x)
        if f_x is not None:
            self.puntos_iteracion.append(self.canvas.ax.plot(x, f_x, 'go', label='x')[0])

        self.canvas.ax.legend()
        self.canvas.draw()
