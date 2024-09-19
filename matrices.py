class Matriz:
    def __init__(self, filas, columnas):
        # Inicializar una matriz vacía con las dimensiones especificadas
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

    def mostrar(self):
        # Mostrar la matriz de manera legible
        resultado = ""
        for fila in self.matriz:
            resultado += str(fila) + "\n"
        return resultado

    def redondear_convertir(self, valor, precision, tolerancia):
        valor_redondeado = round(valor, precision)
        if abs(valor_redondeado - round(valor_redondeado)) < tolerancia:
            return int(round(valor_redondeado))
        return valor_redondeado

    @staticmethod
    def format_expression(terms):
        expr = ""
        for idx, term in enumerate(terms):
            if idx == 0:
                expr += str(term)
            else:
                if term >= 0:
                    expr += f" + {term}"
                else:
                    expr += f" - {abs(term)}"
        return expr

    # Función para representar vectores con una "caja" de contorno
    @staticmethod
    def box_vector(vector, title=""):
        # Convertir números a cadenas y encontrar la longitud máxima
        number_strings = [str(num) for num in vector]
        max_num_length = max(len(s) for s in number_strings)
        max_line_length = max(max_num_length, len(title)) + 2  # Añadir espacio para los márgenes

        # Construir la parte superior de la caja
        result = f"┌{'─' * max_line_length}┐\n"
        if title:
            result += f"│ {title.center(max_line_length - 2)} │\n"
            result += f"├{'─' * max_line_length}┤\n"

        # Añadir cada elemento del vector
        for num_str in number_strings:
            result += f"│ {num_str.rjust(max_line_length - 2)} │\n"

        # Construir la parte inferior de la caja
        result += f"└{'─' * max_line_length}┘\n"

        return result
    
    @staticmethod
    def box_vector_horizontal(vector, title=""):
        # Convertir números a cadenas y encontrar la longitud máxima
        number_strings = [str(num) for num in vector]
        max_num_length = max(len(s) for s in number_strings)
        total_width = len(vector) * (max_num_length + 1) + (len(vector) - 1)

        # Construir la parte superior de la caja
        result = f"┌{'─' * total_width}┐\n"
        if title:
            centered_title = title.center(total_width)
            result += f"│{centered_title}│\n"
            result += f"├{'─' * total_width}┤\n"

        # Añadir los elementos del vector en una sola línea
        row_str = " ".join(f"{num.rjust(max_num_length)}" for num in number_strings)
        result += f"│ {row_str} │\n"

        # Construir la parte inferior de la caja
        result += f"└{'─' * total_width}┘\n"

        return result

    def eliminacion_gauss_jordan(self, precision=4, tolerancia=1e-2):
        n = self.filas
        m = self.columnas
        pasos = "Matriz Inicial:\n" + self.mostrar()

        fila_pivote = 0
        for col in range(m - 1):
            if fila_pivote >= n:
                break

            # Encontrar el máximo en la columna actual para cambiar filas
            fila_max = fila_pivote
            for k in range(fila_pivote + 1, n):
                if abs(self.matriz[k][col]) > abs(self.matriz[fila_max][col]):
                    fila_max = k

            # Intercambiar filas si es necesario
            if self.matriz[fila_max] != self.matriz[fila_pivote]:
                self.matriz[fila_pivote], self.matriz[fila_max] = self.matriz[fila_max], self.matriz[fila_pivote]
                pasos += f"\nCambiar fila {fila_pivote + 1} con fila {fila_max + 1}:\n" + self.mostrar()

            pivote = self.matriz[fila_pivote][col]
            if abs(pivote) < tolerancia:
                # Si el pivote es cero, continuar con la siguiente columna
                continue

            # Dividir la fila del pivote por el escalar para volverlo 1
            for j in range(col, m):
                self.matriz[fila_pivote][j] = self.redondear_convertir(
                    self.matriz[fila_pivote][j] / pivote, precision, tolerancia)
            pasos += f"\nFila {fila_pivote + 1} / {pivote}:\n" + self.mostrar()

            # Eliminar elementos en otras filas
            for i in range(n):
                if i != fila_pivote:
                    factor = self.matriz[i][col]
                    for k in range(col, m):
                        self.matriz[i][k] = self.redondear_convertir(
                            self.matriz[i][k] - factor * self.matriz[fila_pivote][k], precision, tolerancia)
                    pasos += f"\nFila {i + 1} - fila {fila_pivote + 1} * {factor}:\n" + self.mostrar()
            fila_pivote += 1

        # Calcular las soluciones después de la eliminación
        soluciones = self.calcular_soluciones_general()
        return self.matriz, pasos, soluciones

    def calcular_soluciones_general(self):
        n = self.filas
        m = self.columnas
        soluciones_texto = []
        pivotes = {}
        variables_libres = []

        for i in range(n):
            fila = self.matriz[i]
            # Identificar la posición del pivote en la fila
            pivot_col = None
            for j in range(m - 1):
                if abs(fila[j]) > 1e-12:
                    pivot_col = j
                    break
            if pivot_col is None:
                if abs(fila[-1]) > 1e-12:
                    soluciones_texto.append("Sistema inconsistente")
                    return "\n".join(soluciones_texto)  # Salir si el sistema es inconsistente
                else:
                    continue
            pivotes[pivot_col] = i

        # Identificar variables libres: columnas que no son pivotes
        all_vars = set(range(m - 1))
        pivot_vars = set(pivotes.keys())
        free_vars = all_vars - pivot_vars

        # Generar soluciones
        for pivot_col in sorted(pivotes.keys()):
            i = pivotes[pivot_col]
            coef = self.matriz[i]
            solucion = f"x{pivot_col + 1} = {coef[-1]}"
            for j in range(pivot_col + 1, m - 1):
                if abs(coef[j]) > 1e-12:
                    # Cambiar el signo según el valor de coef[j]
                    if coef[j] > 0:
                        solucion += f" - {abs(coef[j])}*x{j + 1}"
                    else:
                        solucion += f" + {abs(coef[j])}*x{j + 1}"
            soluciones_texto.append(solucion)

        for var in sorted(free_vars):
            soluciones_texto.append(f"x{var + 1} = variable libre")

        if not soluciones_texto:
            soluciones_texto.append("Sistema con soluciones infinitas o sin solución única")

        return "\n".join(soluciones_texto)

    @staticmethod
    def sumar_vectores(*vectores):

        if not vectores:
            raise ValueError("Se debe proporcionar al menos un vector.")

        longitud = len(vectores[0])
        for vector in vectores:
            if len(vector) != longitud:
                raise ValueError("Todos los vectores deben tener la misma longitud.")

        resultado = [0] * longitud
        pasos = "Pasos de la suma de vectores:\n"

        # Construir la representación vertical de los vectores con caja
        vectores_verticales = [Matriz.box_vector(vector, title=f"Vector {i+1}") for i, vector in enumerate(vectores)]
        pasos += "\n".join(vectores_verticales) + "\n"

        # Sumar componentes y construir detalle
        pasos += "Suma de componentes:\n"
        for i in range(longitud):
            elementos = [vector[i] for vector in vectores]
            suma_elemento = sum(elementos)
            resultado[i] = suma_elemento
            # Formatear expresión
            suma_detalle = Matriz.format_expression(elementos)
            pasos += f"Componente {i+1}: {suma_detalle} = {suma_elemento}\n"

        pasos += "\nResultado final:\n"
        pasos += Matriz.box_vector(resultado)

        return resultado, pasos

    @staticmethod
    def combinar_vectores(escalars, vectors):
        
        if not vectors or not escalars:
            raise ValueError("Se deben proporcionar al menos un escalar y un vector.")
        if len(escalars) != len(vectors):
            raise ValueError("El número de escalares y vectores debe ser el mismo.")

        longitud = len(vectors[0])
        for vector in vectors:
            if len(vector) != longitud:
                raise ValueError("Todos los vectores deben tener la misma longitud.")

        resultado = [0] * longitud
        pasos = "Pasos de la combinación de vectores:\n"

        # Mostrar los vectores multiplicados por sus escalares
        vectores_escalados = []
        for idx, (escalar, vector) in enumerate(zip(escalars, vectors)):
            vector_escalado = [escalar * v for v in vector]
            vectores_escalados.append(vector_escalado)
            pasos += f"\nEscalar {idx+1} ({escalar}) * Vector {idx+1}:\n"
            # Mostrar vector original con caja
            pasos += Matriz.box_vector(vector, title=f"Vector {idx+1}")
            # Mostrar vector escalado con caja
            pasos += "Vector escalado:\n"
            pasos += Matriz.box_vector(vector_escalado) + "\n"

        # Sumar los vectores escalados
        pasos += "Suma de los vectores escalados:\n"
        for i in range(longitud):
            elementos = [vector[i] for vector in vectores_escalados]
            suma_elemento = sum(elementos)
            resultado[i] = suma_elemento
            # Formatear expresión
            suma_detalle = Matriz.format_expression(elementos)
            pasos += f"Componente {i+1}: {suma_detalle} = {suma_elemento}\n"

        # Añadir el resultado final con caja
        pasos += "\nResultado final:\n"
        pasos += Matriz.box_vector(resultado)

        return resultado, pasos
    
    @staticmethod
    def producto_vector_fila_por_vector_columna(vector_fila, vector_columna):

        if len(vector_fila) != len(vector_columna):
            raise ValueError("Los vectores deben tener la misma longitud.")

        pasos = "Cálculo del producto de vector fila por vector columna:\n"

        # Mostrar el vector fila y el vector columna con cajas
        pasos += "\nVector Fila:\n"
        pasos += Matriz.box_vector_horizontal(vector_fila)

        pasos += "\nVector Columna:\n"
        pasos += Matriz.box_vector(vector_columna)

        # Calcular cada multiplicación individual y acumular el resultado
        productos_individuales = []
        for vf, vc in zip(vector_fila, vector_columna):
            producto = vf * vc
            productos_individuales.append(producto)

        # Mostrar los productos individuales
        pasos += "\nProductos individuales:\n"
        for i, (vf, vc, prod) in enumerate(zip(vector_fila, vector_columna, productos_individuales)):
            pasos += f"Elemento {i+1}: {vf} * {vc} = {prod}\n"

        # Calcular la suma total
        resultado = sum(productos_individuales)
        suma_detalle = Matriz.format_expression(productos_individuales)
        pasos += f"\nSuma de los productos individuales:\n{suma_detalle} = {resultado}\n"

        return resultado, pasos