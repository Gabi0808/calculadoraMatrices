from utilidades import *
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

    def eliminacion_gauss_jordan(self, precision=4, tolerancia=1e-2):
        gestor = GestorPasos()
        gestor.agregar_paso("Matriz Inicial:", matriz=self)

        fila_pivote = 0
        for col in range(self.columnas - 1):
            if fila_pivote >= self.filas:
                break

            fila_max = fila_pivote
            for k in range(fila_pivote + 1, self.filas):
                if abs(self.matriz[k][col]) > abs(self.matriz[fila_max][col]):
                    fila_max = k

            if self.matriz[fila_max] != self.matriz[fila_pivote]:
                self.matriz[fila_pivote], self.matriz[fila_max] = self.matriz[fila_max], self.matriz[fila_pivote]
                gestor.agregar_paso(f"Cambiar fila {fila_pivote + 1} con fila {fila_max + 1}:", matriz=self)

            pivote = self.matriz[fila_pivote][col]
            if abs(pivote) < tolerancia:
                continue

            for j in range(col, self.columnas):
                self.matriz[fila_pivote][j] = self.redondear_convertir(
                    self.matriz[fila_pivote][j] / pivote, precision, tolerancia)
            gestor.agregar_paso(f"Fila {fila_pivote + 1} / {pivote}:", matriz=self)

            for i in range(self.filas):
                if i != fila_pivote:
                    factor = self.matriz[i][col]
                    for k in range(col, self.columnas):
                        self.matriz[i][k] = self.redondear_convertir(
                            self.matriz[i][k] - factor * self.matriz[fila_pivote][k], precision, tolerancia)
                    gestor.agregar_paso(f"Fila {i + 1} - fila {fila_pivote + 1} * {factor}:", matriz=self)

            fila_pivote += 1

        fila_pivote += 1

        soluciones = self.calcular_soluciones_general()
        return self.matriz, gestor.mostrar_pasos(), soluciones
    
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

        # Mostrar la matriz 1
        pasos_gestor.agregar_paso("Matriz 1:", self.mostrar())
        # Mostrar la matriz 2
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