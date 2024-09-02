class Matriz:
    def __init__(self, filas, columnas):
        # Inicializar una matriz vacía con las dimensiones especificadas
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

    @staticmethod
    def obtener_matriz_desde_entrada():
        # Método estático para crear una matriz desde la entrada del usuario
        n = int(input("Ingrese el número de ecuaciones: "))
        m = n + 1
        matriz = Matriz(n, m)

        for i in range(n):
            print(f"Ecuación {i + 1}:")
            for j in range(m):
                if j == m - 1:
                    matriz.matriz[i][j] = float(input("Ingrese el término independiente: "))
                else:
                    matriz.matriz[i][j] = float(input(f"Ingrese el coeficiente de la variable {j + 1}: "))

        return matriz

    def mostrar(self):
        # Mostrar la matriz de manera legible
        for fila in self.matriz:
            print(fila)

    def gauss_jordan_eliminacion(self, precision=4, tolerancia=1e-2):
        # Implementación de la eliminación Gauss-Jordan con la lógica existente
        def redondear_convertir(valor, precision, tolerancia):
            valor_redondeado = round(valor, precision)
            if abs(valor_redondeado - round(valor_redondeado)) < tolerancia:
                return int(round(valor_redondeado))
            return valor_redondeado

        n = self.filas
        m = self.columnas

        print("\nMatriz Inicial:")
        self.mostrar()

        for i in range(n):
            # Encontrar el máximo en la columna para cambiar filas
            fila_max = i
            for k in range(i + 1, n):
                if abs(self.matriz[k][i]) > abs(self.matriz[fila_max][i]):
                    fila_max = k

            # Intercambiar filas
            if self.matriz[fila_max] != self.matriz[i]:
                self.matriz[i], self.matriz[fila_max] = self.matriz[fila_max], self.matriz[i]
                print(f"\nCambiar fila {i + 1} con fila {fila_max + 1}:")
                self.mostrar()
        

            pivote = self.matriz[i][i]
            if pivote == 0:
                raise ValueError("La matriz es inconsistente y no puede ser resuelta.")

            # Dividir la fila del pivote por el escalar para volverlo 1
            for j in range(i, m):
                self.matriz[i][j] = redondear_convertir(self.matriz[i][j] / pivote, precision, tolerancia)

            print(f"\nFila {i + 1} / {pivote}:")
            self.mostrar()

            # Eliminar elementos abajo y arriba del pivote
            for j in range(n):
                if j != i:
                    factor = self.matriz[j][i]
                    for k in range(i, m):
                        self.matriz[j][k] = redondear_convertir(self.matriz[j][k] - factor * self.matriz[i][k], precision, tolerancia)

                    print(f"\nFila {j + 1} - fila {i + 1} * {factor}:")
                    self.mostrar()

        return self.matriz


if __name__ == "__main__":
    # Crear una matriz desde la entrada del usuario
    matriz = Matriz.obtener_matriz_desde_entrada()
    # Realizar la eliminación Gauss-Jordan
    resultado = matriz.gauss_jordan_eliminacion()
    print("\nMatriz reducida a matriz de identidad:")
    matriz.mostrar()
