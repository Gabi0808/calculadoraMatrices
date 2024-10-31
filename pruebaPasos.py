import functools
from utilidades import *

def registrar_pasos_condicional(nombre_operacion):
    """
    Decorador que registra los pasos solo si el gestor de pasos está activo.
    """
    def decorador(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if getattr(self, 'registro_activo', False):
                self.gestor.agregar_paso(f"Iniciando {nombre_operacion}:", matriz=self)

            resultado = func(self, *args, **kwargs)

            if getattr(self, 'registro_activo', False):
                self.gestor.agregar_paso(f"Finalizando {nombre_operacion}:", matriz=self)

            return resultado
        return wrapper
    return decorador


class Matriz:
    def __init__(self, filas, columnas, matriz=None):
        self.filas = filas
        self.columnas = columnas
        self.matriz = matriz if matriz else [[0 for _ in range(columnas)] for _ in range(filas)]
        self.gestor = GestorPasos()  # El gestor de pasos se inicializa aquí
        self.registro_activo = False  # Por defecto, el registro está desactivado

    def activar_registro(self):
        """Activa el registro de pasos."""
        self.registro_activo = True

    def desactivar_registro(self):
        """Desactiva el registro de pasos."""
        self.registro_activo = False

    @registrar_pasos_condicional("Eliminación Gauss-Jordan")
    def eliminacion_gauss_jordan(self, precision=4, tolerancia=1e-2, matriz_aumentada=None):
        fila_pivote = 0
        for col in range(self.columnas):
            if fila_pivote >= self.filas:
                break

            # Encontrar el pivote
            fila_max = fila_pivote
            for k in range(fila_pivote + 1, self.filas):
                if abs(self.matriz[k][col]) > abs(self.matriz[fila_max][col]):
                    fila_max = k

            # Intercambiar filas
            if self.matriz[fila_max] != self.matriz[fila_pivote]:
                self.matriz[fila_pivote], self.matriz[fila_max] = self.matriz[fila_max], self.matriz[fila_pivote]

            pivote = self.matriz[fila_pivote][col]
            if abs(pivote) < tolerancia:
                continue

            # Dividir la fila pivote por el pivote
            for j in range(col, self.columnas):
                self.matriz[fila_pivote][j] /= pivote

            # Eliminar las otras filas
            for i in range(self.filas):
                if i != fila_pivote:
                    factor = self.matriz[i][col]
                    for k in range(col, self.columnas):
                        self.matriz[i][k] -= factor * self.matriz[fila_pivote][k]

            fila_pivote += 1

        return self.matriz
    
    def mostrar(self):
        return MatrizHelper.box_matrix(self.matriz)

# Crear una instancia de Matriz
matriz = Matriz(3, 3, [[2, 1, 1], [1, 3, 2], [1, 0, 0]])

# Activar el registro de pasos
matriz.activar_registro()

# Ejecutar la función con el registro activo
matriz.eliminacion_gauss_jordan()

# Mostrar los pasos
print(matriz.gestor.mostrar_pasos())

# Desactivar el registro de pasos
matriz.desactivar_registro()

# Ejecutar nuevamente la función sin registrar los pasos
matriz= matriz.eliminacion_gauss_jordan()

