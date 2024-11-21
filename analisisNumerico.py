import sympy as sym
import re

class Funcion:
    
    def __init__(self, funcion, variable=None) -> None:
        funcion_procesada = self._preprocesar_funcion(funcion)
        self.funcion = sym.sympify(funcion_procesada)
        
        if not isinstance(self.funcion, sym.Expr):
            raise ValueError("La función ingresada no es válida. Asegúrate de ingresar una expresión matemática correcta.")
        
        self.variable = variable if variable is not None else sym.symbols('x')
        
    
    def _preprocesar_funcion(self, funcion_str):
        funcion_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion_str)
        funcion_str = re.sub(r'(sin|cos|tan|log|exp|sqrt)([a-zA-Z])', r'\1(\2)', funcion_str)
        return funcion_str

    def evaluar_funcion(self, valor):
        if isinstance(valor, (int, float)):
            try:
                resultado = self.funcion.subs(self.variable, valor)
                return float(resultado.evalf())
            except Exception as e:
                print(f"Error al evaluar la función en {valor}: {e}")
                return None
        else:
            print(f"Advertencia: Se intentó evaluar un valor no numérico: {valor}")
            return None
        
    def evaluar_derivada(self, valor):
        derivada = sym.diff(self.funcion, self.variable)
        try:
            resultado = derivada.subs(self.variable, valor)
            return float(resultado.evalf())
        except Exception as e:
            print(f"Error al evaluar la derivada en {valor}: {e}")
            return None

    @staticmethod
    def calcular_error_relativo(x_nuevo, x_anterior):
        return abs((x_nuevo - x_anterior) / x_nuevo) * 100 if x_nuevo != 0 else float('inf')

    def biseccion(self, a, b, tolerancia=1e-6):
        registro = "Iteración del método de bisección:\n"
        puntos = []
        c_anterior = a
        iteracion = 1
        while abs(b - a) / 2 > tolerancia:
            c = (a + b) / 2 
            f_c = self.evaluar_funcion(c)

            if f_c is None:
                registro += f"Error al evaluar c en iteración {iteracion}\n"
                break
            
            if f_c == 0:
                registro += f"Iteración {iteracion}: c = {c}, Raíz exacta encontrada.\n"
                puntos.append((a, b, c))
                return c, registro, puntos

            error = self.calcular_error_relativo(c, c_anterior)
            registro += f"Iteración {iteracion}: c = {c}, Error absoluto = {error:.6f}%\n"
            puntos.append((a, b, c))

            if self.evaluar_funcion(a) * f_c < 0:
                b = c
            else:
                a = c

            c_anterior = c
            iteracion += 1

        raiz_aproximada = (a + b) / 2
        registro += f"\nRaíz aproximada encontrada: {raiz_aproximada}"
        puntos.append((a, b, raiz_aproximada))
        return raiz_aproximada, registro, puntos

    def biseccion_multiple(self, a, b, subintervalos=10, tolerancia=1e-6):
        intervalo_longitud = (b - a) / subintervalos
        raices = []
        registros = []
        puntos_por_raiz = []
        
        for i in range(subintervalos):
            a_i = a + i * intervalo_longitud
            b_i = a + (i + 1) * intervalo_longitud
            
            if self.evaluar_funcion(a_i) * self.evaluar_funcion(b_i) < 0:
                raiz, registro, puntos = self.biseccion(a_i, b_i, tolerancia)
                raices.append(raiz)
                registros.append(registro)
                puntos_por_raiz.append(puntos)
        
        return raices, registros, puntos_por_raiz

    def newton_raphson(self, x0, tolerancia=1e-6, max_iteraciones=100):
        registro = "Iteración del método de Newton-Raphson:\n"
        iteracion = 1
        x_anterior = x0
        puntos = []  # Lista para almacenar los puntos de cada iteración

        while iteracion <= max_iteraciones:
            f_x = self.evaluar_funcion(x_anterior)
            f_x_derivada = self.evaluar_derivada(x_anterior)

            if f_x_derivada == 0:
                registro += f"Iteración {iteracion}: Derivada cero, no se puede continuar.\n"
                break

            x_nuevo = x_anterior - f_x / f_x_derivada
            error = self.calcular_error_relativo(x_nuevo, x_anterior)
            puntos.append((x_anterior, x_nuevo, error))  # Guardar el punto actual y el error en la lista

            registro += f"Iteración {iteracion}: x = {x_nuevo}, Error relativo = {error:.6f}%\n"

            if error < tolerancia:
                registro += f"\nEl método converge en la iteración {iteracion}. La raíz aproximada es: {x_nuevo}\n"
                return x_nuevo, registro, puntos

            x_anterior = x_nuevo
            iteracion += 1

        registro += "\nNo se alcanzó la tolerancia especificada dentro del número máximo de iteraciones."
        return None, registro, puntos
    
    def falsa_posicion(self, a, b, tolerancia=1e-6, max_iteraciones=100):
        registro = "Iteración del método de Falsa Posición:\n"
        puntos = []
        iteracion = 1
        c_anterior = a
        
        while iteracion <= max_iteraciones:
            f_a = self.evaluar_funcion(a)
            f_b = self.evaluar_funcion(b)
            
            if f_a * f_b > 0:
                registro += "Error: Los extremos a y b no encierran una raíz.\n"
                return None, registro, puntos
            
            if f_b - f_a == 0:
                registro += "Error: División por cero en la fórmula de c.\n"
                return None, registro, puntos
            
            c = b - f_b * (b - a) / (f_b - f_a)
            f_c = self.evaluar_funcion(c)
            
            puntos.append((a, b, c))
            
            error = abs(c - c_anterior)
            registro += f"Iteración {iteracion}: a = {a}, b = {b}, c = {c}, f(c) = {f_c}, Error absoluto = {error:.6e}\n"
            
            if abs(f_c) < tolerancia or error < tolerancia:
                registro += f"\nRaíz aproximada encontrada: {c} en iteración {iteracion}.\n"
                return c, registro, puntos
            
            if f_a * f_c < 0:
                b = c
                f_b = f_c
            else:
                a = c
                f_a = f_c
            
            c_anterior = c
            iteracion += 1
        
        registro += f"\nLímite de iteraciones alcanzado ({max_iteraciones}). Raíz aproximada: {c_anterior}\n"
        return c_anterior, registro, puntos
    

    def secante(self, x0, x1, tolerancia=1e-6, max_iter=100):
        registro = ""
        puntos_por_raiz = []

        for iteracion in range(max_iter):
            f_x0 = self.evaluar_funcion(x0)
            f_x1 = self.evaluar_funcion(x1)

            if f_x1 - f_x0 == 0:
                registro += f"\nDivisión por cero detectada en la iteración {iteracion}. El método se detiene.\n"
                break

            x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
            puntos_por_raiz.append((x0, x1))

            # Registrar la iteración
            registro += f"Iteración {iteracion}: x0={x0}, x1={x1}, x2={x2}\n"


            if abs(x2 - x1) < tolerancia:
                registro += f"\nRaíz aproximada encontrada: {x2}\n"
                return x2, registro, puntos_por_raiz

            x0, x1 = x1, x2

        registro += "\nNo se encontró una raíz en el límite de iteraciones.\n"
        return None, registro, puntos_por_raiz
