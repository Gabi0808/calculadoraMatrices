import sympy as sym
import re

class Funcion:
    
    def __init__(self, funcion, variable=None) -> None:
        funcion_procesada = self._preprocesar_funcion(funcion)
        self.funcion = sym.sympify(funcion_procesada)
        
        if variable is not None:
            self.variable = variable
        else:
            self.variable = sym.symbols('x')
    
    def _preprocesar_funcion(self, funcion_str):
        funcion_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion_str)
        funcion_str = re.sub(r'(sin|cos|tan|registro|exp|sqrt)([a-zA-Z])', r'\1(\2)', funcion_str)
        return funcion_str

    def evaluar_funcion(self, valor):
        funcion_eval = self.funcion.subs(self.variable, valor)
        return funcion_eval.evalf()

    @staticmethod
    def calcular_error_relativo(x_nuevo, x_anterior):
        if x_nuevo == 0:
            raise ValueError("x_nuevo no puede ser cero, ya que dividir entre cero no es válido.")
        
        error_relativo = abs((x_nuevo - x_anterior) / x_nuevo) * 100
        return error_relativo

    def biseccion(self, a, b, tolerancia=1e-6):
        if self.evaluar_funcion(a) * self.evaluar_funcion(b) > 0:
            raise ValueError("La función no cambia de signo en el intervalo dado. No se puede aplicar el método de bisección.")
        
        registro = "Iteración del método de bisección:\n"
        c_anterior = a
        iteracion = 1  # Contador de iteraciones

        while abs(b - a) / 2 > tolerancia:
            c = (a + b) / 2 

            # Evaluar la función en c y calcular el error relativo
            if self.evaluar_funcion(c) == 0:
                registro += f"Iteración {iteracion}: c = {c}, Raíz exacta encontrada.\n"
                return c, registro

            error = self.calcular_error_relativo(c, c_anterior)
            registro += f"Iteración {iteracion}: c = {c}, Error relativo = {error:.6f}%\n"

            # Actualizar el intervalo según el cambio de signo
            if self.evaluar_funcion(c) * self.evaluar_funcion(a) < 0:
                b = c
            else:
                a = c

            c_anterior = c
            iteracion += 1  # Incrementar el contador

        # Resultado final después de las iteraciones
        raiz_aproximada = (a + b) / 2
        registro += f"\nRaíz aproximada encontrada: {raiz_aproximada}"
        return raiz_aproximada, registro
