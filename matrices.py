from utilidades import MatrizHelper, GestorPasos, Formateador
from vectores import Vector

class Matriz:
    def __init__(self, filas, columnas, matriz=None):
        self.filas = filas
        self.columnas = columnas
        if matriz is not None:
            self.matriz = matriz
        else:
            self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

    def mostrar(self):
        return MatrizHelper.box_matrix(self.matriz)

    def redondear_convertir(self, valor, precision, tolerancia):
        valor_redondeado = round(valor, precision)
        if abs(valor_redondeado - round(valor_redondeado)) < tolerancia:
            return int(round(valor_redondeado))
        return valor_redondeado

    def eliminacion_gauss_jordan(self, precision=4, tolerancia=1e-2, matriz_aumentada=None):
        
        gestor = GestorPasos()
        gestor.agregar_paso("Matriz Inicial:", matriz=self)

        if matriz_aumentada:
            gestor.agregar_paso("Matriz aumentada inicial:", matriz=matriz_aumentada)

        fila_pivote = 0
        for col in range(self.columnas):
            if fila_pivote >= self.filas:
                break

            # Encontrar el pivote
            fila_max = fila_pivote
            for k in range(fila_pivote + 1, self.filas):
                if abs(self.matriz[k][col]) > abs(self.matriz[fila_max][col]):
                    fila_max = k

            # Intercambiar filas si es necesario
            if self.matriz[fila_max] != self.matriz[fila_pivote]:
                self.matriz[fila_pivote], self.matriz[fila_max] = self.matriz[fila_max], self.matriz[fila_pivote]
                if matriz_aumentada:
                    matriz_aumentada.matriz[fila_pivote], matriz_aumentada.matriz[fila_max] = matriz_aumentada.matriz[fila_max], matriz_aumentada.matriz[fila_pivote]
                gestor.agregar_paso(f"Intercambiar fila {fila_pivote + 1} con fila {fila_max + 1}:", matriz=self)
                if matriz_aumentada:
                    gestor.agregar_paso(f"Intercambio correspondiente en matriz aumentada:", matriz=matriz_aumentada)

            pivote = self.matriz[fila_pivote][col]
            if abs(pivote) < tolerancia:
                continue

            # Normalizar la fila pivote tanto en la matriz original como en la aumentada
            for j in range(col, self.columnas):
                self.matriz[fila_pivote][j] = self.redondear_convertir(self.matriz[fila_pivote][j] / pivote, precision, tolerancia)
            if matriz_aumentada:
                for j in range(matriz_aumentada.columnas):
                    matriz_aumentada.matriz[fila_pivote][j] = self.redondear_convertir(matriz_aumentada.matriz[fila_pivote][j] / pivote, precision, tolerancia)
            gestor.agregar_paso(f"Fila {fila_pivote + 1} / {pivote}:", matriz=self)
            if matriz_aumentada:
                gestor.agregar_paso(f"Fila aumentada {fila_pivote + 1} / {pivote}:", matriz=matriz_aumentada)

            # Eliminar las otras filas
            for i in range(self.filas):
                if i != fila_pivote:
                    factor = self.matriz[i][col]
                    for k in range(col, self.columnas):
                        self.matriz[i][k] = self.redondear_convertir(self.matriz[i][k] - factor * self.matriz[fila_pivote][k], precision, tolerancia)
                    if matriz_aumentada:
                        for k in range(matriz_aumentada.columnas):
                            matriz_aumentada.matriz[i][k] = self.redondear_convertir(matriz_aumentada.matriz[i][k] - factor * matriz_aumentada.matriz[fila_pivote][k], precision, tolerancia)
                    gestor.agregar_paso(f"Fila {i + 1} - fila {fila_pivote + 1} * {factor}:", matriz=self)
                    if matriz_aumentada:
                        gestor.agregar_paso(f"Fila aumentada {i + 1} - fila {fila_pivote + 1} * {factor}:", matriz=matriz_aumentada)

            fila_pivote += 1

        if matriz_aumentada:
            return self.matriz, matriz_aumentada.matriz, gestor.mostrar_pasos()
        else:
            return self.matriz, gestor.mostrar_pasos()
    
    def calcular_soluciones_general(self):
        n = self.filas
        m = self.columnas
        soluciones_texto = []
        pivotes = {}
        
        for i in range(n):
            fila = self.matriz[i]
            col_pivote = None
            for j in range(m - 1):
                if abs(fila[j]) > 1e-12:
                    col_pivote = j
                    break
            if col_pivote is None:
                if abs(fila[-1]) > 1e-12:
                    soluciones_texto.append("Sistema inconsistente")
                    return "\n".join(soluciones_texto)
                else:
                    continue
            pivotes[col_pivote] = i
        
        variables_totales = set(range(m - 1))
        variables_pivote = set(pivotes.keys())
        variables_libres = variables_totales - variables_pivote
        
        for col_pivote in sorted(pivotes.keys()):
            i = pivotes[col_pivote]
            coef = self.matriz[i]
            solucion = f"x{col_pivote + 1} = {coef[-1]}"
            for j in range(col_pivote + 1, m - 1):
                if abs(coef[j]) > 1e-12:
                    if coef[j] > 0:
                        solucion += f" - {abs(coef[j])}*x{j + 1}"
                    else:
                        solucion += f" + {abs(coef[j])}*x{j + 1}"
            soluciones_texto.append(solucion)
        
        for var in sorted(variables_libres):
            soluciones_texto.append(f"x{var + 1} = variable libre")
        if not soluciones_texto:
            soluciones_texto.append("Sistema con soluciones infinitas o sin solución única")
        return "\n".join(soluciones_texto)
    
    
    def multiplicar_matriz_por_vector(self, vector):
        if self.columnas != vector.dimension:
            raise ValueError("El número de columnas de la matriz debe coincidir con la dimensión del vector.")
        
        # Asegurarnos que el vector tenga orientación vertical
        if vector.orientacion != "vertical":
            vector = vector.cambiar_orientacion()
        
        resultado = []
        gestor_pasos = GestorPasos()
        gestor_pasos.agregar_paso("Multiplicación de matriz por vector:")

        for i in range(self.filas):
            fila = Vector(self.columnas, self.matriz[i], orientacion="horizontal")
            producto, pasos = fila.producto_vector_fila_por_vector_columna(vector)
            resultado.append(producto)
            gestor_pasos.agregar_paso(f"Resultado de fila {i + 1}: {pasos}")
        
        resultado_final = Vector(len(resultado), resultado, orientacion="vertical")
        gestor_pasos.agregar_paso("Resultado final después de sumar las filas:", vector=Formateador.box_vector(resultado_final.vector))
        
        return resultado, gestor_pasos.mostrar_pasos()
    
    def escalar_matriz(self, escalar=1):
        nueva_matriz = [
            [float(elemento) * escalar for elemento in fila] for fila in self.matriz
            ]
        return Matriz(self.filas, self.columnas, nueva_matriz)
    
    @staticmethod
    def sumar_matrices(*matrices):
        if not matrices:
            raise ValueError("Se debe proporcionar al menos una matriz")
        if not all(isinstance(m, Matriz) for m in matrices):
            raise ValueError("Todos los argumentos deben ser instancias de la clase Matriz")
        
        filas = matrices[0].filas
        columnas = matrices[0].columnas
        for matriz in matrices:
            if matriz.filas != filas or matriz.columnas != columnas:
                raise ValueError("Todas las matrices deben de tener las mismas filas y columnas")
        
        resultado = [[0 for _ in range(columnas)] for _ in range(filas)]
        
        gestor = GestorPasos()
        
        gestor.agregar_paso("Pasos de la suma de matrices:")
        for i, matriz in enumerate(matrices):
            gestor.agregar_paso(f"Matriz {i+1}:")
            gestor.agregar_paso(matriz.mostrar())
        
        for i in range(filas):
            for j in range(columnas):
                elementos = [matriz.matriz[i][j] for matriz in matrices]
                suma_elemento = sum(elementos)
                resultado[i][j] = suma_elemento
                suma_detalle = " + ".join(map(str, elementos))
                gestor.agregar_paso(f"Componente ({i + 1}, {j + 1}): {suma_detalle} = {suma_elemento}")
        
        matriz_resultado = Matriz(filas, columnas, resultado)
        
        gestor.agregar_paso("Resultado de la suma de matrices:")
        gestor.agregar_paso(matriz_resultado.mostrar())
        
        return matriz_resultado, gestor.mostrar_pasos()
    
    @staticmethod
    def transponer_matriz(matriz):
        if not isinstance(matriz, Matriz):
            raise ValueError("El argumento debe ser una instancia de la clase Matriz")
        
        transpuesta = [[matriz.matriz[j][i] for j in range(matriz.filas)] for i in range(matriz.columnas)]
        
        matriz_transpuesta = Matriz(matriz.columnas, matriz.filas, transpuesta)
        
        return matriz_transpuesta
    
    def multiplicar_matrices(self, otra_matriz):
        if self.columnas != otra_matriz.filas:
            raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.")

        resultado = Matriz(self.filas, otra_matriz.columnas)
        pasos_gestor = GestorPasos()
        pasos_gestor.agregar_paso("Inicio de la multiplicación de matrices:")

        pasos_gestor.agregar_paso("Matriz 1:", self.mostrar())

        pasos_gestor.agregar_paso("Matriz 2:", otra_matriz.mostrar())

        for i in range(self.filas):
            for j in range(otra_matriz.columnas):
                suma_productos = 0
                detalles_productos = []
                for k in range(self.columnas):
                    producto = self.matriz[i][k] * otra_matriz.matriz[k][j]
                    suma_productos += producto
                    detalles_productos.append(f"({self.matriz[i][k]} * {otra_matriz.matriz[k][j]})")
                resultado.matriz[i][j] = suma_productos
                detalles_productos_str = " + ".join(detalles_productos)
                pasos_gestor.agregar_paso(f"Elemento ({i + 1}, {j + 1}) calculado como suma de productos: {detalles_productos_str} = {suma_productos}", resultado.mostrar())

        pasos_gestor.agregar_paso("Resultado final de la multiplicación de matrices:", resultado.mostrar())
        return resultado, pasos_gestor.mostrar_pasos()
    
    def calcular_determinante(self, precision=4, tolerancia=1e-2):
        if self.filas != self.columnas:
            raise ValueError("El determinante solo se puede calcular para matrices cuadradas.")
        
        # Crear una copia de la matriz para no modificar la original
        matriz_temp = [fila[:] for fila in self.matriz]
        n = self.filas
        signo = 1
        gestor = GestorPasos()
        
        # Agregar el primer paso con la matriz inicial
        gestor.agregar_paso("Inicio del cálculo del determinante:", matriz=Matriz(n, n, matriz_temp))

        for i in range(n):
            # Buscar el pivote en la columna actual
            max_fila = i
            for k in range(i + 1, n):
                if abs(matriz_temp[k][i]) > abs(matriz_temp[max_fila][i]):
                    max_fila = k

            # Intercambiar filas si es necesario
            if i != max_fila:
                matriz_temp[i], matriz_temp[max_fila] = matriz_temp[max_fila], matriz_temp[i]
                signo *= -1
                gestor.agregar_paso(f"Intercambiar fila {i + 1} con fila {max_fila + 1}. Signo del determinante = {signo}", matriz=Matriz(n, n, matriz_temp))

            # Si el pivote es cero, el determinante es cero
            if abs(matriz_temp[i][i]) < 1e-12:
                gestor.agregar_paso(f"El pivote en la diagonal ({i + 1}, {i + 1}) es cero. El determinante es 0", matriz=Matriz(n, n, matriz_temp))
                return 0, gestor.mostrar_pasos()

            # Reducir las filas debajo del pivote
            for j in range(i + 1, n):
                factor = matriz_temp[j][i] / matriz_temp[i][i]
                factor = self.redondear_convertir(factor, precision, tolerancia)  # Redondear el factor
                for k in range(i, n):
                    matriz_temp[j][k] -= factor * matriz_temp[i][k]
                    matriz_temp[j][k] = self.redondear_convertir(matriz_temp[j][k], precision, tolerancia)
                gestor.agregar_paso(f"Reducir fila {j + 1} usando fila {i + 1} con factor {factor}", matriz=Matriz(n, n, matriz_temp))

        # Calcular el determinante como el producto de la diagonal multiplicado por el signo
        determinante = signo
        for i in range(n):
            determinante *= matriz_temp[i][i]
            determinante = self.redondear_convertir(determinante, precision, tolerancia)
        gestor.agregar_paso(f"Producto de la diagonal para el cálculo final del determinante: {determinante}", matriz=Matriz(n, n, matriz_temp))

        return determinante, gestor.mostrar_pasos()

    
    def resolver_cramer(self, vector_constantes, precision=4, tolerancia=1e-2):
        if self.filas != self.columnas:
            raise ValueError("La matriz debe ser cuadrada para aplicar la regla de Cramer.")
        
        if self.filas != len(vector_constantes):
            raise ValueError("El vector de constantes debe tener la misma dimensión que la matriz.")
        
        determinante, pasos_determinante = self.calcular_determinante(precision, tolerancia)
        
        if determinante == 0:
            mensaje_error = "El sistema no tiene una solución ya que el determinante de la matriz de coeficientes es 0."
            return None, mensaje_error  # Retorna None para soluciones y un mensaje de error
        
        soluciones = []
        gestor = GestorPasos()
        gestor.agregar_paso("Inicio de la solución por Regla de Cramer", matriz=self)
        gestor.agregar_paso("Vector de constantes:", vector=Formateador.box_vector(vector_constantes))
        gestor.agregar_paso(f"Determinante de la matriz original: {determinante}")
        
        for i in range(self.columnas):
            matriz_reemplazo = [fila[:] for fila in self.matriz]
            
            # Reemplazar la columna i por el vector de constantes
            for j in range(self.filas):
                matriz_reemplazo[j][i] = vector_constantes[j]
            
            matriz_temp = Matriz(self.filas, self.columnas, matriz_reemplazo)
            gestor.agregar_paso(f"Matriz temporal al reemplazar la columna {i + 1} con el vector de constantes:", matriz=matriz_temp)
            
            # Calcular el determinante de la matriz temporal
            det_reemplazo, pasos_reemplazo = matriz_temp.calcular_determinante(precision, tolerancia)
            gestor.agregar_paso(f"Determinante de la matriz temporal con columna {i + 1} reemplazada: {det_reemplazo}")
            
            # Detalle de la división para el cálculo de x_i
            valor_variable = det_reemplazo / determinante
            gestor.agregar_paso(f"Cálculo de x{i + 1}: {det_reemplazo} / {determinante} = {valor_variable}")
            
            # Redondear el resultado
            valor_variable = self.redondear_convertir(valor_variable, precision, tolerancia)
            soluciones.append(valor_variable)
            
            gestor.agregar_paso(f"Valor redondeado de x{i + 1}: {valor_variable}")
        
        return soluciones, gestor.mostrar_pasos()

    def calcular_inversa(self, precision=4, tolerancia=1e-2):

        # Paso 1: Comprobar si la matriz es cuadrada
        if self.filas != self.columnas:
            raise ValueError("La matriz debe ser cuadrada para tener inversa.")
        
        # Paso 2: Comprobar si el determinante es diferente de 0
        determinante, pasos_det = self.calcular_determinante(precision, tolerancia)
        if determinante == 0:
            raise ValueError("La matriz no tiene inversa porque su determinante es 0.")
        
        # Paso 3: Crear la matriz identidad de las mismas dimensiones
        identidad = Matriz(self.filas, self.columnas)
        for i in range(self.filas):
            identidad.matriz[i][i] = 1

        # Paso 4: Aplicar eliminación Gauss-Jordan a la matriz original y la identidad
        _, inversa, pasos = self.eliminacion_gauss_jordan(precision=precision, tolerancia=tolerancia, matriz_aumentada=identidad)

        for i in range(self.filas):
            for j in range(self.columnas):
                inversa[i][j] = self.redondear_convertir(inversa[i][j], precision, tolerancia)

        return Matriz(self.filas, self.columnas, inversa), pasos