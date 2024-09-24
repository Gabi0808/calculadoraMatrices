from utilidades import *

class Vector:
    def __init__(self, dimension, vector=None, escalar=1):
        self.dimension = dimension
        self.escalar = escalar
        if vector is not None:
            if len(vector) != dimension:
                raise ValueError("La longitud del vector no coincide con la dimensión proporcionada.")
            self.vector = vector
        else:
            self.vector = [0 for _ in range(dimension)]

    def escalar_vector(self):
        self.vector = [elemento * self.escalar for elemento in self.vector]
        
    @staticmethod
    def sumar_vectores(*vectores):
        if not vectores:
            raise ValueError("Se debe proporcionar al menos un vector.")
        if not all(isinstance(v, Vector) for v in vectores):
            raise ValueError("Todos los argumentos deben ser instancias de la clase Vector.")

        longitud = vectores[0].dimension
        for vector in vectores:
            if vector.dimension != longitud:
                raise ValueError("Todos los vectores deben tener la misma longitud.")

        resultado = [0] * longitud
        gestor = GestorPasos()

        gestor.agregar_paso("Pasos de la suma de vectores:")
        for i, vector in enumerate(vectores):
            gestor.agregar_paso(f"Vector {i + 1}:", vector=Formateador.box_vector(vector.vector))

        # Escalar los vectores
        for i, vector in enumerate(vectores):
            vector.escalar_vector()
            gestor.agregar_paso(f"Vector {i + 1} escalado:", vector=Formateador.box_vector(vector.vector))
        
        for i in range(longitud):
            elementos = [vector.vector[i] for vector in vectores]
            suma_elemento = sum(elementos)
            resultado[i] = suma_elemento
            suma_detalle = Formateador.format_expression(elementos)
            gestor.agregar_paso(f"Componente {i + 1}: {suma_detalle} = {suma_elemento}")

        gestor.agregar_paso("Resultado final:", Formateador.box_vector(resultado))
        return resultado, gestor.mostrar_pasos()

    def producto_vector_fila_por_vector_columna(self, otro_vector):
        # Verificar que la longitud de los vectores coincida
        if self.dimension != otro_vector.dimension:
            raise ValueError("Los vectores deben tener la misma longitud.")

        gestor_pasos = GestorPasos()
        # Mostrar el vector fila y el vector columna utilizando Formateador y GestorPasos
        gestor_pasos.agregar_paso("Cálculo del producto de vector fila por vector columna:")

        gestor_pasos.agregar_paso("Vector Fila:", vector=Formateador.box_vector_horizontal(self.vector))
        gestor_pasos.agregar_paso("Vector Columna:", vector=Formateador.box_vector(otro_vector.vector))

        # Calcular cada multiplicación individual y acumular el resultado
        productos_individuales = []
        for vf, vc in zip(self.vector, otro_vector.vector):
            producto = vf * vc
            productos_individuales.append(producto)

        # Mostrar los productos individuales
        gestor_pasos.agregar_paso("Productos individuales:")
        for i, (vf, vc, prod) in enumerate(zip(self.vector, otro_vector.vector, productos_individuales)):
            gestor_pasos.agregar_paso(f"Elemento {i + 1}: {vf} * {vc} = {prod}")

        # Calcular la suma total
        resultado = sum(productos_individuales)
        suma_detalle = Formateador.format_expression(productos_individuales)
        gestor_pasos.agregar_paso(f"Suma de los productos individuales: {suma_detalle} = {resultado}")

        return resultado, gestor_pasos.mostrar_pasos()
    