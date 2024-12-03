from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSplitter,QMessageBox, QTableWidget)
from PyQt5.QtCore import Qt, QTimer
import sympy as sym
from analisisNumerico import Funcion
from interfazHelper import InterfazHelperAnalisisNumerico, RenderThread

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
        
        entradas_layout.addLayout(contenedor_funcion)

        entradas_layout.addLayout(contenedor_intervalos)
        
        self.table_widget_resultado = QTableWidget()
        self.label_raiz = QLabel()

        entradas_layout.addWidget(self.boton_calcular)
        entradas_layout.addWidget(self.boton_siguiente)
        entradas_layout.addWidget(self.label_raiz)
        entradas_layout.addWidget(self.table_widget_resultado)

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

        self.timer = QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.actualizar_latex_async)
        self.render_thread = None

    def actualizar_latex(self):
        self.timer.start()

    def actualizar_latex_async(self):
        self.timer.stop()
        funcion_texto = self.input_funcion.text()
        try:
            self.funcion = Funcion(funcion_texto)
            latex_str = sym.latex(self.funcion.funcion)
            
            if self.render_thread is None or not self.render_thread.isRunning():
                self.render_thread = RenderThread(latex_str)
                self.render_thread.update_image_signal.connect(self.mostrar_imagen)
                self.render_thread.start()
                
            self.graficar_funcion_async()
            
        except Exception:
            self.latex_label.clear()

    def mostrar_imagen(self, pixmap):
        self.latex_label.setPixmap(pixmap)

    def calcular_biseccion_multiple(self):
        try:
            funcion_texto = self.input_funcion.text()
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            self.funcion = Funcion(funcion_texto)

            if self.funcion.dominio.contains(a) & self.funcion.dominio.contains(b): 
                self.raices, self.puntos_por_raiz, self.tablas = self.funcion.biseccion_multiple(a, b, subintervalos=10, tolerancia=1e-6)
                self.raiz_actual = 0
                self.iteracion_actual = 0
                if self.raices:
                    self.boton_siguiente.setEnabled(True)
                    self.label_raiz.setText(f"Raiz aproximada: {self.raices[self.raiz_actual]:.6g}")
                    self.label_raiz.setContentsMargins(15, 15, 15, 15)
                    header = ["Iteración", "a", "b", "c", "Error Relativo"]
                    InterfazHelperAnalisisNumerico.modificar_tabla(self.tablas[self.raiz_actual], self.table_widget_resultado, header)

                    # Pasar los valores de a, b, c de la primera iteración a actualizar_grafico
                    a, b, c = self.puntos_por_raiz[self.raiz_actual][self.iteracion_actual]
                    self.actualizar_grafico(a, b, c)
                else:
                    QMessageBox.information(self, "Resultado", "No se encontraron raíces.")
            else:
                QMessageBox.information(self, "Entradas", "Alguna de las entradas no pertenece al dominio.") 
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
                header = ["Iteración", "a", "b", "c", "Error Relativo"]
                InterfazHelperAnalisisNumerico.modificar_tabla(self.tablas[self.raiz_actual], self.table_widget_resultado, header)

            else:
                QMessageBox.information(self, "Fin", "Todas las iteraciones han terminado.")
                self.boton_siguiente.setEnabled(False)
                return
        
        a, b, c = self.puntos_por_raiz[self.raiz_actual][self.iteracion_actual]
        self.actualizar_grafico(a, b, c)

    def graficar_funcion_async(self):

        for line in self.canvas.ax.get_lines():
            line.remove()

        x_min, x_max = self.xlim
        num_points = 1000
        x_vals = [x_min + i * (x_max - x_min) / (num_points - 1) for i in range(num_points)]
        
        x_vals_filtrados = [x for x in x_vals if self.funcion.dominio.contains(x)]

        # Evaluar los valores de la función para los valores de x filtrados
        y_vals = []
        for x in x_vals_filtrados:
            try:
                y_vals.append(self.funcion.evaluar_funcion(x))
            except Exception as e:
                print(f"Error al evaluar la función en x={x}: {e}")
                
        self.canvas.ax.plot(x_vals_filtrados, y_vals, label="f(x)", color='blue')
        self.canvas.ax.axhline(0, color='black', linewidth=0.7)
        self.canvas.ax.axvline(0, color='black', linewidth=0.7)
        #self.canvas.ax.set_xlim(self.xlim)
        #self.canvas.ax.set_ylim(self.ylim)
        self.canvas.ax.set_xlim(self.initial_xlim)
        self.canvas.ax.set_ylim(self.initial_ylim)
        self.canvas.ax.set_aspect('equal', adjustable='box')
        self.canvas.ax.legend()
        self.canvas.draw()

    def actualizar_grafico(self, a, b, c):
        if not hasattr(self, 'grafico_fijo'):
            self.graficar_funcion_async()
            self.grafico_fijo = True

        if hasattr(self, 'puntos_iteracion'):
                for p in self.puntos_iteracion:
                    try:
                        p.remove()
                    except ValueError:
                        pass
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

        self.puntos_iteracion.append(self.canvas.ax.plot([], [], ' ', label=f'Iteración actual: {self.iteracion_actual}')[0])
        
        self.canvas.ax.legend()
        self.canvas.draw()

class NewtonRaphsonTab(QWidget):
    def __init__(self):
        super().__init__()

        splitter = QSplitter(Qt.Horizontal)

        entradas_widget = QWidget()
        entradas_layout = QVBoxLayout(entradas_widget)
        entradas_layout.setAlignment(Qt.AlignTop)

        contenedor_funcion, self.input_funcion, self.latex_label = InterfazHelperAnalisisNumerico.crear_funcion_input_latex(texto="Ingrese la función en términos de 'x':",callback_actualizar_latex= self.actualizar_latex)
        
        contenedor_inicial = QVBoxLayout() 
        self.input_x0 = InterfazHelperAnalisisNumerico.crear_input("Ingrese el valor inicial 'x0':")
        contenedor_inicial.addWidget(self.input_x0)

        self.boton_calcular = InterfazHelperAnalisisNumerico.crear_boton("Calcular Newton-Raphson", self.calcular_newton_raphson)
        self.boton_siguiente = InterfazHelperAnalisisNumerico.crear_boton("Siguiente Iteración", self.siguiente_iteracion)
        self.boton_siguiente.setEnabled(False)
        
        self.text_edit_resultado = InterfazHelperAnalisisNumerico.crear_text_edit()
        self.table_widget_resultado = QTableWidget()
        self.label_raiz = QLabel()
        
        entradas_layout.addLayout(contenedor_funcion)
        entradas_layout.addLayout(contenedor_inicial)
        entradas_layout.addWidget(self.boton_calcular)
        entradas_layout.addWidget(self.boton_siguiente)
        entradas_layout.addWidget(self.label_raiz)
        entradas_layout.addWidget(self.table_widget_resultado)

        grafico_widget, self.canvas = InterfazHelperAnalisisNumerico.crear_canvas_widget(self)

        splitter.addWidget(entradas_widget)
        splitter.addWidget(grafico_widget)

        splitter.setSizes([900, 800])

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(splitter)

        self.iteraciones = []
        self.iteracion_actual = 0
        self.x_actual = 0

        self.xlim = (-50, 50)
        self.ylim = (-50, 50)
        self.initial_xlim = (-5, 5)
        self.initial_ylim = (-5, 5)

        self.timer = QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.actualizar_latex_async)
        self.render_thread = None

    def actualizar_latex(self):
        self.timer.start()

    def actualizar_latex_async(self):
        self.timer.stop()
        funcion_texto = self.input_funcion.text()
        try:
            self.funcion = Funcion(funcion_texto)
            latex_str = sym.latex(self.funcion.funcion)
            
            if self.render_thread is None or not self.render_thread.isRunning():
                self.render_thread = RenderThread(latex_str)
                self.render_thread.update_image_signal.connect(self.mostrar_imagen)
                self.render_thread.start()
                
            self.graficar_funcion_async()
            
        except Exception:
            self.latex_label.clear()

    def mostrar_imagen(self, pixmap):
        self.latex_label.setPixmap(pixmap)

    def calcular_newton_raphson(self):
        try:
            funcion_texto = self.input_funcion.text()
            x0 = float(self.input_x0.text())
            self.funcion = Funcion(funcion_texto)
            
            if self.funcion.dominio.contains(x0):

                self.raiz, self.iteraciones, self.tabla = self.funcion.newton_raphson(x0, tolerancia=1e-6)
                self.iteracion_actual = 0 

                if self.raiz is not None:
                    self.boton_siguiente.setEnabled(True)
                    self.label_raiz.setText(f"Raiz aproximada: {self.raiz:.6g}")
                    self.label_raiz.setContentsMargins(15, 15, 15, 15)
                    header = ["Iteración", "x","f'(x)","Error Relativo"]
                    InterfazHelperAnalisisNumerico.modificar_tabla(self.tabla, self.table_widget_resultado, header)
                
                    # Graficar los puntos de la primera iteración
                    x0, x1, error = self.iteraciones[self.iteracion_actual]
                    self.actualizar_grafico(x0)
                
                else:
                    QMessageBox.information(self, "Resultado", "No se encontró una raíz con el método Newton-Raphson.")

            else:
                QMessageBox.information(self, "Entrada", "El valor inicial no pertenece al dominio.") 
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada no válida: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def siguiente_iteracion(self):
        if self.iteracion_actual < len(self.iteraciones) - 1:
            self.iteracion_actual += 1
            x_anterior, x_nuevo, _ = self.iteraciones[self.iteracion_actual]
            self.actualizar_grafico(x_nuevo)
        else:
            QMessageBox.information(self, "Fin", "Todas las iteraciones han terminado.")
            self.boton_siguiente.setEnabled(False)

    def graficar_funcion_async(self):
        
        for line in self.canvas.ax.get_lines():
            line.remove()

        x_min, x_max = self.xlim
        num_points = 1000
        x_vals = [x_min + i * (x_max - x_min) / (num_points - 1) for i in range(num_points)]
        
        x_vals_filtrados = [x for x in x_vals if self.funcion.dominio.contains(x)]

        # Evaluar los valores de la función para los valores de x filtrados
        y_vals = []
        for x in x_vals_filtrados:
            try:
                y_vals.append(self.funcion.evaluar_funcion(x))
            except Exception as e:
                print(f"Error al evaluar la función en x={x}: {e}")

        self.canvas.ax.plot(x_vals_filtrados, y_vals, label="f(x)", color='blue')
        self.canvas.ax.axhline(0, color='black', linewidth=0.7)
        self.canvas.ax.axvline(0, color='black', linewidth=0.7)
        self.canvas.ax.set_xlim(self.initial_xlim)
        self.canvas.ax.set_ylim(self.initial_ylim)
        self.canvas.ax.legend()
        self.canvas.draw()

    def actualizar_grafico(self, x):
        if not hasattr(self, 'grafico_fijo'):
            self.graficar_funcion_async()
            self.grafico_fijo = True

        if hasattr(self, 'puntos_iteracion'):
            for p in self.puntos_iteracion:
                try:
                    p.remove()
                except ValueError:
                    pass
        self.puntos_iteracion = []

        f_x = self.funcion.evaluar_funcion(x)
        f_x_derivada = self.funcion.evaluar_derivada(x)

        if f_x is not None:
            self.puntos_iteracion.append(self.canvas.ax.plot(x, f_x, 'go', label='x')[0])

        if f_x is not None and f_x_derivada is not None:

            tangente_x_vals = [x - 1, x + 1]
            tangente_y_vals = [f_x + f_x_derivada * (t - x) for t in tangente_x_vals]
            
            self.puntos_iteracion.append(
                self.canvas.ax.plot(tangente_x_vals, tangente_y_vals, 'r--', label="Tangente")[0]
            )

        self.canvas.ax.legend()
        self.canvas.draw()

class FalsaPosicionTab(QWidget):
    def __init__(self):
        super().__init__()

        splitter = QSplitter(Qt.Horizontal)

        entradas_widget = QWidget()
        entradas_layout = QVBoxLayout(entradas_widget)
        entradas_layout.setAlignment(Qt.AlignTop)

        contenedor_funcion, self.input_funcion, self.latex_label = InterfazHelperAnalisisNumerico.crear_funcion_input_latex(texto="Ingrese la función en términos de 'x':",callback_actualizar_latex= self.actualizar_latex)
        
        contenedor_intervalos, self.input_a, self.input_b = InterfazHelperAnalisisNumerico.crear_intervalos_input("Ingrese el valor de 'a':","Ingrese el valor de 'b':")

        self.boton_calcular = InterfazHelperAnalisisNumerico.crear_boton("Calcular Falsa Posición", self.calcular_falsa_posicion)
        self.boton_siguiente = InterfazHelperAnalisisNumerico.crear_boton("Siguiente Iteración", self.siguiente_iteracion)
        self.boton_siguiente.setEnabled(False)
        
        self.table_widget_resultado = QTableWidget()

        entradas_layout.addLayout(contenedor_funcion)
        entradas_layout.addLayout(contenedor_intervalos)
        entradas_layout.addWidget(self.boton_calcular)
        entradas_layout.addWidget(self.boton_siguiente)
        self.label_raiz = QLabel()
        entradas_layout.addWidget(self.label_raiz)
        entradas_layout.addWidget(self.table_widget_resultado)

        grafico_widget, self.canvas = InterfazHelperAnalisisNumerico.crear_canvas_widget(self)

        splitter.addWidget(entradas_widget)
        splitter.addWidget(grafico_widget)

        splitter.setSizes([900, 800])

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(splitter)

        self.iteracion_actual = 0
        self.x_actual = 0
        self.registro = ""

        self.xlim = (-50, 50)
        self.ylim = (-50, 50)
        self.initial_xlim = (-5, 5)
        self.initial_ylim = (-5, 5)

        self.timer = QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.actualizar_latex_async)
        self.render_thread = None

    def actualizar_latex(self):
        self.timer.start()

    def actualizar_latex_async(self):
        """
        Actualiza el contenido LaTeX de la función ingresada. Si no es válida,
        simplemente detiene el proceso sin mostrar errores.
        """
        self.timer.stop()
        funcion_texto = self.input_funcion.text()
        try:
            # Intenta crear la función
            self.funcion = Funcion(funcion_texto)
            latex_str = sym.latex(self.funcion.funcion)
            
            # Renderizar el LaTeX solo si la función es válida
            if self.render_thread is None or not self.render_thread.isRunning():
                self.render_thread = RenderThread(latex_str)
                self.render_thread.update_image_signal.connect(self.mostrar_imagen)
                self.render_thread.start()

            # Graficar la función
            self.graficar_funcion_async()

        except Exception:
            # Si hay un error, simplemente detén la actualización
            self.funcion = None  # Marca la función como inválida
            self.latex_label.clear()  # Limpia cualquier representación previa

    def mostrar_imagen(self, pixmap):
        self.latex_label.setPixmap(pixmap)

    def calcular_falsa_posicion(self):
        """
        Calcula el método de falsa posición. Si la función no es válida, 
        detiene el proceso y registra el error.
        """
        try:
            funcion_texto = self.input_funcion.text()
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            self.funcion = Funcion(funcion_texto)
            
            if self.funcion.dominio.contains(a) & self.funcion.dominio.contains(b):

                self.raiz, self.puntos_por_raiz, self.tabla = self.funcion.falsa_posicion(a, b, tolerancia=1e-6)
                self.iteracion_actual = 0
                if self.raiz:
                    self.boton_siguiente.setEnabled(True)
                    self.label_raiz.setText(f"Raiz aproximada: {self.raiz:.6g}")
                    self.label_raiz.setContentsMargins(15, 15, 15, 15)
                    header = ["Iteración", "a", "b", "c", "f(c)","Error Relativo"]
                    InterfazHelperAnalisisNumerico.modificar_tabla(self.tabla, self.table_widget_resultado, header)

                    # Pasar los valores de a, b, c de la primera iteración a actualizar_grafico
                    a, b, c = self.puntos_por_raiz[self.iteracion_actual]
                    self.actualizar_grafico(a, b, c)
                else:
                    QMessageBox.information(self, "Resultado", "No se encontró una raíz con el método Falsa Posicion.")
            else:
                QMessageBox.information(self, "Entradas", "Algunas de las entradas no son parte del dominio de la funcion.")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada no válida: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def siguiente_iteracion(self):
        if self.iteracion_actual < len(self.puntos_por_raiz) - 1:
            self.iteracion_actual += 1
            a, b, c = self.puntos_por_raiz[self.iteracion_actual]
            self.actualizar_grafico(a, b, c)
        else:
            QMessageBox.information(self, "Fin", "Todas las iteraciones han terminado.")
            self.boton_siguiente.setEnabled(False)

    def graficar_funcion_async(self):

        for line in self.canvas.ax.get_lines():
            line.remove()

        x_min, x_max = self.xlim
        num_points = 1000
        x_vals = [x_min + i * (x_max - x_min) / (num_points - 1) for i in range(num_points)]
        
        x_vals_filtrados = [x for x in x_vals if self.funcion.dominio.contains(x)]

        # Evaluar los valores de la función para los valores de x filtrados
        y_vals = []
        for x in x_vals_filtrados:
            try:
                y_vals.append(self.funcion.evaluar_funcion(x))
            except Exception as e:
                print(f"Error al evaluar la función en x={x}: {e}")
                
        # Graficar la función
        self.canvas.ax.plot(x_vals_filtrados, y_vals, label="f(x)", color='blue')
        self.canvas.ax.axhline(0, color='black', linewidth=0.7)
        self.canvas.ax.axvline(0, color='black', linewidth=0.7)
        self.canvas.ax.set_xlim(self.initial_xlim)
        self.canvas.ax.set_ylim(self.initial_ylim)
        self.canvas.ax.set_aspect('equal', adjustable='box')
        self.canvas.ax.legend()
        self.canvas.draw()

    def actualizar_grafico(self, a, b, c):
        if not hasattr(self, 'grafico_fijo'):
            self.graficar_funcion_async()
            self.grafico_fijo = True

        # Limpiar puntos de la iteración anterior
        if hasattr(self, 'puntos_iteracion'):
            for p in self.puntos_iteracion:
                try:
                    p.remove()
                except ValueError:
                    pass
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
        
class SecanteTab(QWidget):
    def __init__(self):
        super().__init__()

        splitter = QSplitter(Qt.Horizontal)

        # Panel izquierdo (Entradas)
        entradas_widget = QWidget()
        entradas_layout = QVBoxLayout(entradas_widget)
        entradas_layout.setAlignment(Qt.AlignTop)

        # Crear entradas para función, valores iniciales y botones
        contenedor_funcion, self.input_funcion, self.latex_label = InterfazHelperAnalisisNumerico.crear_funcion_input_latex(
            texto="Ingrese la función en términos de 'x':",
            callback_actualizar_latex=self.actualizar_latex
        )
        contenedor_intervalos, self.input_x0, self.input_x1 = InterfazHelperAnalisisNumerico.crear_intervalos_input(
            "Ingrese el valor de x₀:",
            "Ingrese el valor de x₁:"
        )

        self.boton_calcular = InterfazHelperAnalisisNumerico.crear_boton(
            "Calcular Método de la Secante",
            self.calcular_secante
        )
        self.boton_siguiente = InterfazHelperAnalisisNumerico.crear_boton(
            "Siguiente Iteración",
            self.siguiente_iteracion
        )
        self.boton_siguiente.setEnabled(False)

        # Campo para mostrar resultados
        #self.text_edit_resultado = InterfazHelperAnalisisNumerico.crear_text_edit()
        self.table_widget_resultado = QTableWidget()
        self.label_raiz = QLabel()

        # Agregar widgets al layout de entrada
        entradas_layout.addLayout(contenedor_funcion)
        entradas_layout.addLayout(contenedor_intervalos)
        entradas_layout.addWidget(self.boton_calcular)
        entradas_layout.addWidget(self.boton_siguiente)
        #entradas_layout.addWidget(QLabel("Registro de iteraciones:"))
        entradas_layout.addWidget(self.label_raiz)
        entradas_layout.addWidget(self.table_widget_resultado)

        # Panel derecho (Gráficos)
        grafico_widget, self.canvas = InterfazHelperAnalisisNumerico.crear_canvas_widget(self)

        splitter.addWidget(entradas_widget)
        splitter.addWidget(grafico_widget)
        splitter.setSizes([900, 800])

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(splitter)

        # Variables de control
        self.iteracion_actual = 0
        self.x_prev = 0
        self.x_curr = 0
        self.registro = ""
        self.xlim = (-50, 50)
        self.ylim = (-50, 50)
        self.initial_xlim = (-5, 5)
        self.initial_ylim = (-5, 5)

        self.timer = QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.actualizar_latex_async)
        self.render_thread = None

    def actualizar_latex(self):
        self.timer.start()

    def actualizar_latex_async(self):
        self.timer.stop()
        funcion_texto = self.input_funcion.text()
        try:
            self.funcion = Funcion(funcion_texto)
            latex_str = sym.latex(self.funcion.funcion)
            
            if self.render_thread is None or not self.render_thread.isRunning():
                self.render_thread = RenderThread(latex_str)
                self.render_thread.update_image_signal.connect(self.mostrar_imagen)
                self.render_thread.start()
                
            self.graficar_funcion_async()
            
        except Exception:
            self.latex_label.clear()

    def mostrar_imagen(self, pixmap):
        self.latex_label.setPixmap(pixmap)

    def calcular_secante(self):
        try:
            funcion_texto = self.input_funcion.text()
            x0 = float(self.input_x0.text())
            x1 = float(self.input_x1.text())
            self.funcion = Funcion(funcion_texto)

            if self.funcion.dominio.contains(x0) & self.funcion.dominio.contains(x1):
                self.raiz, self.puntos_por_raiz, self.tabla = self.funcion.secante(x0, x1, tolerancia=1e-6)
                self.iteracion_actual = 0
                
                if self.raiz:
                    self.boton_siguiente.setEnabled(True)
                    self.label_raiz.setText(f"Raiz aproximada: {self.raiz:.6g}")
                    self.label_raiz.setContentsMargins(15, 15, 15, 15)
                    header = ["Iteración", "x0", "x1", "x2", "Error Relativo"]
                    InterfazHelperAnalisisNumerico.modificar_tabla(self.tabla, self.table_widget_resultado, header)

                    # Graficar los puntos de la primera iteración
                    x_prev, x_curr = self.puntos_por_raiz[self.iteracion_actual]
                    self.actualizar_grafico(x_prev, x_curr)
                else:
                    QMessageBox.information(self, "Resultado", "No se encontraron raíces.")
            else:
                QMessageBox.information(self, "Entradas", "Algunas de las entradas no son parte del dominio de la funcion.")
            

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Entrada no válida: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def siguiente_iteracion(self):
        if self.iteracion_actual < len(self.puntos_por_raiz) - 1:
            self.iteracion_actual += 1
            x_prev, x_curr = self.puntos_por_raiz[self.iteracion_actual]
            self.actualizar_grafico(x_prev, x_curr)
        else:
            QMessageBox.information(self, "Fin", "Todas las iteraciones han terminado.")
            self.boton_siguiente.setEnabled(False)

    def graficar_funcion_async(self):

        for line in self.canvas.ax.get_lines():
            line.remove()

        x_min, x_max = self.xlim
        num_points = 1000
        x_vals = [x_min + i * (x_max - x_min) / (num_points - 1) for i in range(num_points)]
        
        x_vals_filtrados = [x for x in x_vals if self.funcion.dominio.contains(x)]

        # Evaluar los valores de la función para los valores de x filtrados
        y_vals = []
        for x in x_vals_filtrados:
            try:
                y_vals.append(self.funcion.evaluar_funcion(x))
            except Exception as e:
                print(f"Error al evaluar la función en x={x}: {e}")

        self.canvas.ax.plot(x_vals_filtrados, y_vals, label="f(x)", color='blue')
        self.canvas.ax.axhline(0, color='black', linewidth=0.7)
        self.canvas.ax.axvline(0, color='black', linewidth=0.7)
        #self.canvas.ax.set_xlim(self.xlim)
        #self.canvas.ax.set_ylim(self.ylim)
        self.canvas.ax.set_xlim(self.initial_xlim)
        self.canvas.ax.set_ylim(self.initial_ylim)
        self.canvas.ax.set_aspect('equal', adjustable='box')
        self.canvas.ax.legend()
        self.canvas.draw()

    def actualizar_grafico(self, x_prev, x_curr):
        if not hasattr(self, 'grafico_fijo'):
            self.graficar_funcion_async()
            self.grafico_fijo = True

        if hasattr(self, 'linea_secante') and self.linea_secante:
            try:
                self.linea_secante.remove()
            except ValueError:
                pass
            self.linea_secante = None

        # Limpiar puntos de la iteración anterior
        if hasattr(self, 'puntos_iteracion'):
            for p in self.puntos_iteracion:
                try:
                    p.remove()
                except ValueError:
                    pass
        self.puntos_iteracion = []

        # Graficar puntos de la iteración actual
        f_x_prev = self.funcion.evaluar_funcion(x_prev)
        f_x_curr = self.funcion.evaluar_funcion(x_curr)

        if f_x_prev is not None:
            self.puntos_iteracion.append(self.canvas.ax.plot(x_prev, f_x_prev, 'ro', label='x_prev')[0])
        if f_x_curr is not None:
            self.puntos_iteracion.append(self.canvas.ax.plot(x_curr, f_x_curr, 'go', label='x_curr')[0])

        if f_x_prev is not None and f_x_curr is not None:
            self.linea_secante = self.canvas.ax.plot(
                [x_prev, x_curr], [f_x_prev, f_x_curr], 'k--', label='Secante'
            )[0] 
        self.canvas.ax.legend()
        self.canvas.draw()
