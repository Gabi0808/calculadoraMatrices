from utilidades import * 
from vectores import Vector

class Matriz:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

    def mostrar(self):
        resultado = ""
        for fila in self.matriz:
            resultado += str(fila) + "\n"
        return resultado

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
        
        resultado = [0] * self.filas
        gestor_pasos = GestorPasos()
        gestor_pasos.agregar_paso("Multiplicación de matriz por vector:")

        for i in range(self.filas):
            fila = Vector(self.columnas, self.matriz[i])
            producto, pasos = fila.producto_vector_fila_por_vector_columna(vector)
            resultado[i] = producto
            gestor_pasos.agregar_paso(f"Resultado de fila {i + 1}: {pasos}")
        
        gestor_pasos.agregar_paso("Resultado final:", vector=Formateador.box_vector(resultado))
        return resultado, gestor_pasos.mostrar_pasos()
