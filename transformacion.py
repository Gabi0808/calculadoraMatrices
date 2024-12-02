from matplotlib.patches import Polygon
from matrices import Matriz, Vector

class Transformacion:
    def __init__(self, matriz: Matriz, vector: Vector):
        self.matriz = matriz
        self.vector = vector

    def interpolar_puntos(self, punto_inicial, punto_final, t):
        """Interpolación lineal entre dos puntos representados por objetos Vector."""
        # Acceder a los valores del vector usando el atributo `vector` del objeto Vector
        return [
            (1 - t) * punto_inicial.vector[0] + t * punto_final.vector[0],  # Interpolación en el eje X
            (1 - t) * punto_inicial.vector[1] + t * punto_final.vector[1]   # Interpolación en el eje Y
        ]


    def transformar_vector(self, vector_original, t):
        """Transforma un vector aplicando la matriz de transformación e interpolando."""
        vector_transformado, _ = self.matriz.multiplicar_matriz_por_vector(vector_original)
        return self.interpolar_puntos(vector_original, vector_transformado, t)

    def transformar_area(self, t):
        """Calcula los puntos transformados de un paralelogramo unitario para dibujar el área."""
        origen = [0, 0]
        v1_original = Vector(2,[1, 0])
        v2_original = Vector(2,[0, 1])

        v1_transformado,_ = self.matriz.multiplicar_matriz_por_vector(v1_original)
        v2_transformado,_  = self.matriz.multiplicar_matriz_por_vector(v2_original)

        v1_interpolado = self.interpolar_puntos(v1_original, v1_transformado, t)
        v2_interpolado = self.interpolar_puntos(v2_original, v2_transformado, t)

        return Polygon([origen, v1_interpolado, [v1_interpolado[0] + v2_interpolado[0], 
                                                 v1_interpolado[1] + v2_interpolado[1]], v2_interpolado], 
                       color='yellow', alpha=0.5)

    def transformar_vector_columna(self, t):
        """Transforma el vector columna original aplicando la matriz de transformación."""
        vector_original = self.vector
        vector_transformado, _ = self.matriz.multiplicar_matriz_por_vector(self.vector)
        return self.interpolar_puntos(vector_original, vector_transformado, t)

class Visualizador:
    def __init__(self, transformacion: Transformacion):
        self.transformacion = transformacion
        self.elementos_dinamicos = []  # Lista para almacenar referencias a elementos dinámicos (grid, vector, área)

    def dibujar_vector(self, ax, origen, vector, color):
        # Dibujar el vector con `arrow`
        flecha = ax.arrow(
            origen[0], origen[1],  # Punto de inicio
            vector[0] - origen[0],  # Delta en X
            vector[1] - origen[1],  # Delta en Y
            head_width=0.2, head_length=0.3, fc=color, ec=color, alpha=0.7,
            linewidth=1, zorder=3
        )
        self.elementos_dinamicos.append(flecha)

    def visualizar(self, ax, t):

        # Configurar fondo y ejes básicos (estos no se consideran dinámicos)
        ax.set_facecolor('#1f1f1f')
        ax.grid(color='white', linewidth=0.4, alpha=0.4)
        ax.axhline(0, color='white', linewidth=0.7)
        ax.axvline(0, color='white', linewidth=0.7)

        # Dibujar el área transformada
        area_transformada = self.transformacion.transformar_area(t)
        ax.add_patch(area_transformada)
        self.elementos_dinamicos.append(area_transformada)

        # Dibujar el vector transformado
        vector_transformado = self.transformacion.transformar_vector_columna(t)
        self.dibujar_vector(ax, (0, 0), vector_transformado, 'yellow')
      
        # Redibujar el canvas
        ax.figure.canvas.draw()

    def crear_grid(self, ax, t):
        """Crear un grid transformado basado en la matriz de transformación."""
       # self.borrar_elementos_dinamicos()  # Limpiar elementos existentes del grid

        # Obtener los límites actuales del eje y los ticks
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        x_ticks = ax.get_xticks()
        y_ticks = ax.get_yticks()

        # Calcular el intervalo entre ticks dinámicamente
        x_tick_interval = x_ticks[1] - x_ticks[0] if len(x_ticks) > 1 else (xlim[1] - xlim[0]) / 10
        y_tick_interval = y_ticks[1] - y_ticks[0] if len(y_ticks) > 1 else (ylim[1] - ylim[0]) / 10

        # Extender los límites para incluir un tick adicional en cada dirección
        x_start = x_ticks[0] - x_tick_interval
        x_end = x_ticks[-1] + x_tick_interval
        y_start = y_ticks[0] - y_tick_interval
        y_end = y_ticks[-1] + y_tick_interval

        # Crear líneas verticales basadas en el rango extendido
        x_range = self._generate_ticks(x_start, x_end, x_tick_interval)
        for x in x_range:
            # Puntos inicial y final de la línea vertical
            punto_inicial = Vector(2, [x, y_start])
            punto_final = Vector(2, [x, y_end])

            # Aplicar transformación e interpolación
            punto_inicial_t = self.transformacion.transformar_vector(punto_inicial, t)
            punto_final_t = self.transformacion.transformar_vector(punto_final, t)

            # Dibujar la línea transformada
            linea_v, = ax.plot(
                [punto_inicial_t[0], punto_final_t[0]],
                [punto_inicial_t[1], punto_final_t[1]],
                color='blue', linestyle='-', linewidth=0.7, alpha=0.7
            )
            self.elementos_dinamicos.append(linea_v)

        # Crear líneas horizontales basadas en el rango extendido
        y_range = self._generate_ticks(y_start, y_end, y_tick_interval)
        for y in y_range:
            # Puntos inicial y final de la línea horizontal
            punto_inicial = Vector(2, [x_start, y])
            punto_final = Vector(2, [x_end, y])

            # Aplicar transformación e interpolación
            punto_inicial_t = self.transformacion.transformar_vector(punto_inicial, t)
            punto_final_t = self.transformacion.transformar_vector(punto_final, t)

            # Dibujar la línea transformada
            linea_h, = ax.plot(
                [punto_inicial_t[0], punto_final_t[0]],
                [punto_inicial_t[1], punto_final_t[1]],
                color='blue', linestyle='-', linewidth=0.8, alpha=0.6
            )
            self.elementos_dinamicos.append(linea_h)

            # Asegurar que el aspecto de la gráfica sea igual en ambos ejes
            ax.set_aspect('equal')

    def _generate_ticks(self, start, end, step):
        """Generar ticks extendidos basados en un paso específico."""
        ticks = []
        current = start
        while current <= end:
            ticks.append(round(current, 10))  # Redondear para evitar errores flotantes
            current += step
        return ticks

    def borrar_elementos_dinamicos(self):
        """Eliminar todos los elementos dinámicos del eje."""
        for elemento in self.elementos_dinamicos:
            elemento.remove()  # Eliminar el elemento del eje
        self.elementos_dinamicos.clear()  # Limpiar la lista de elementos
