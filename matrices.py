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

        return self.matriz, pasos
