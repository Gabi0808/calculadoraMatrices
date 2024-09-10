# matrices.py
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

    def gauss_jordan_eliminacion(self, precision=4, tolerancia=1e-2):
        # Implementación de la eliminación Gauss-Jordan con la lógica existente
        def redondear_convertir(valor, precision, tolerancia):
            valor_redondeado = round(valor, precision)
            if abs(valor_redondeado - round(valor_redondeado)) < tolerancia:
                return int(round(valor_redondeado))
            return valor_redondeado

        n = self.filas
        m = self.columnas
        pasos = "Matriz Inicial:\n" + self.mostrar()

        for i in range(n):
            # Encontrar el máximo en la columna para cambiar filas
            fila_max = i
            for k in range(i + 1, n):
                if abs(self.matriz[k][i]) > abs(self.matriz[fila_max][i]):
                    fila_max = k

            # Intercambiar filas si es necesario
            if self.matriz[fila_max] != self.matriz[i]:
                self.matriz[i], self.matriz[fila_max] = self.matriz[fila_max], self.matriz[i]
                pasos += f"\nCambiar fila {i + 1} con fila {fila_max + 1}:\n" + self.mostrar()

            pivote = self.matriz[i][i]
            if pivote == 0:
                raise ValueError("La matriz es inconsistente y no puede ser resuelta.")

            elif pivote != 1:
                # Dividir la fila del pivote por el escalar para volverlo 1
                for j in range(i, m):
                    self.matriz[i][j] = redondear_convertir(self.matriz[i][j] / pivote, precision, tolerancia)
                pasos += f"\nFila {i + 1} / {pivote}:\n" + self.mostrar()

            # Eliminar elementos abajo y arriba del pivote
            for j in range(n):
                if j != i:
                    factor = self.matriz[j][i]
                    for k in range(i, m):
                        self.matriz[j][k] = redondear_convertir(self.matriz[j][k] - factor * self.matriz[i][k], precision, tolerancia)
                    pasos += f"\nFila {j + 1} - fila {i + 1} * {factor}:\n" + self.mostrar()

        # Calcular las soluciones después de la eliminación
        soluciones = self.calcular_soluciones()

        return self.matriz, pasos, soluciones

    def eliminacion_rectangular(self, precision=4, tolerancia=1e-2):
        # Implementación de la eliminación Gauss-Jordan para matrices rectangulares
        def redondear_convertir(valor, precision, tolerancia):
            valor_redondeado = round(valor, precision)
            if abs(valor_redondeado - round(valor_redondeado)) < tolerancia:
                return int(round(valor_redondeado))
            return valor_redondeado

        n = self.filas
        m = self.columnas
        pasos = "Matriz Inicial:\n" + self.mostrar()

        # Implementación de la eliminación escalonada
        fila_pivote = 0
        for col in range(m):
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
                self.matriz[fila_pivote][j] = redondear_convertir(self.matriz[fila_pivote][j] / pivote, precision, tolerancia)
            pasos += f"\nFila {fila_pivote + 1} / {pivote}:\n" + self.mostrar()

            # Eliminar elementos abajo y arriba del pivote
            for i in range(fila_pivote + 1, n):
                factor = self.matriz[i][col]
                for k in range(col, m):
                    self.matriz[i][k] = redondear_convertir(self.matriz[i][k] - factor * self.matriz[fila_pivote][k], precision, tolerancia)
                pasos += f"\nFila {i + 1} - fila {fila_pivote + 1} * {factor}:\n" + self.mostrar()
            
            fila_pivote += 1

        # Calcular las soluciones después de la eliminación
        soluciones = self.calcular_soluciones_rectangular()

        return self.matriz, pasos, soluciones

    def calcular_soluciones(self):
        soluciones = []
        for i in range(self.filas):
            valor = self.matriz[i][-1]  # Obtener el último elemento de cada fila (término independiente)
            soluciones.append(f"x{i + 1} = {valor}")
        return "\n".join(soluciones)

    def calcular_soluciones_rectangular(self):
        # Identificar soluciones de la matriz escalonada, incluyendo variables libres para matrices rectangulares
        n = self.filas
        m = self.columnas
        soluciones = ["x" + str(i) for i in range(m - 1)]  # Considerando que la última columna es el término independiente
        
        # Detectar filas inconsistentes o variables libres
        soluciones_texto = []
        for i in range(n):
            fila = self.matriz[i]
            if all(valor == 0 for valor in fila[:-1]) and fila[-1] != 0:
                soluciones_texto.append("Sistema inconsistente")
                break
            
            # Identificar variables libres
            pivote = next((index for index, valor in enumerate(fila[:-1]) if abs(valor) > 0), None)
            if pivote is not None:
                solucion = f"x{pivote+1} = {fila[-1]}"
                for j in range(pivote + 1, m - 1):
                    if abs(fila[j]) > 0:
                        solucion += f" - {fila[j]}*x{j}"
                soluciones_texto.append(solucion)
        
        if not soluciones_texto:
            soluciones_texto.append("Sistema con soluciones infinitas o sin solución única")
        
        return soluciones_texto