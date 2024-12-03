from sympy import *
from sympy.calculus.util import continuous_domain
import re

class Funcion:
    def __init__(self, funcion, variable=None) -> None:
        funcion_procesada = self._preprocesar_funcion(funcion)
        self.funcion = sympify(funcion_procesada)
        
        if not isinstance(self.funcion, Expr):
            raise ValueError("La función ingresada no es válida. Asegúrate de ingresar una expresión matemática correcta.")
        
        self.variable = variable if variable is not None else symbols('x')
        self.dominio = self.dominio = self.determinar_dominio(self.funcion, self.variable)
    
    def _preprocesar_funcion(self, funcion_str):
        funcion_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion_str)
        funcion_str = re.sub(r'(sin|cos|tan|log|exp|sqrt)([a-zA-Z])', r'\1(\2)', funcion_str)
        return funcion_str

    def es_valor_valido(self, valor):
        """
        Verifica si el valor dado pertenece al dominio de la función en los reales.
        """
        try:
            resultado = self.funcion.subs(self.variable, valor)
            if resultado.is_real is False:
                return False
            return True
        except Exception:
            return False

    def evaluar_funcion(self, valor):           
        try:
            resultado = self.funcion.subs(self.variable, valor)
            if resultado.is_real:
                return float(resultado.evalf())
            else:
                 print(f"El valor {valor} no pertenece al dominio de la función.")
            return None
        except Exception as e:
            print(f"Error al evaluar la función en {valor}: {e}")
            return None
    
    def evaluar_derivada(self, valor):
        if not self.es_valor_valido(valor):
            print(f"El valor {valor} no pertenece al dominio de la función.")
            return None
        derivada = diff(self.funcion, self.variable)
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
        #if not self.es_valor_valido(a) or not self.es_valor_valido(b):
        #    return None, "Uno o ambos valores no pertenecen al dominio de la función.", []
        
        puntos = []
        tabla = []
        c_anterior = a
        iteracion = 1
        while abs(b - a) / 2 > tolerancia:
            c = (a + b) / 2 
            f_c = self.evaluar_funcion(c)

            if f_c is None:
                break
            
            if f_c == 0:
                puntos.append((a, b, c))
                return c, puntos, tabla

            error = self.calcular_error_relativo(c, c_anterior)
            tabla.append([f"{iteracion}", f"{a:.6g}", f"{b:.6g}", f"{c:.6g}", f"{error:.6g}"])
            puntos.append((a, b, c))

            if self.evaluar_funcion(a) * f_c < 0:
                b = c
            else:
                a = c

            c_anterior = c
            iteracion += 1

        raiz_aproximada = (a + b) / 2
        puntos.append((a, b, raiz_aproximada))
        return raiz_aproximada, puntos, tabla

    def biseccion_multiple(self, a, b, subintervalos=10, tolerancia=1e-6):
        intervalo_longitud = (b - a) / subintervalos
        raices = []
        tablas = []
        puntos_por_raiz = []
        
        for i in range(subintervalos):
            a_i = a + i * intervalo_longitud
            b_i = a + (i + 1) * intervalo_longitud
            
            if self.es_valor_valido(a_i) and self.es_valor_valido(b_i):
                if self.evaluar_funcion(a_i) * self.evaluar_funcion(b_i) < 0:
                    raiz, puntos, tabla = self.biseccion(a_i, b_i, tolerancia)
                    raices.append(raiz)
                    tablas.append(tabla)
                    puntos_por_raiz.append(puntos)
        
        return raices, puntos_por_raiz, tablas

    def newton_raphson(self, x0, tolerancia=1e-6, max_iteraciones=100):
        #if not self.es_valor_valido(x0):
         #   return None, "El valor inicial no pertenece al dominio de la función.", []

        iteracion = 1
        x_anterior = x0
        puntos = []
        tabla = []  

        while iteracion <= max_iteraciones:
            f_x = self.evaluar_funcion(x_anterior)
            f_x_derivada = self.evaluar_derivada(x_anterior)

            if f_x_derivada == 0:
                
                break

            x_nuevo = x_anterior - f_x / f_x_derivada
            error = self.calcular_error_relativo(x_nuevo, x_anterior)
            puntos.append((x_anterior, x_nuevo, error))  

            tabla.append([f"{iteracion}", f"{x_nuevo}",f"{f_x_derivada:.6g}", f"{error:.6g}"]) 
            if error < tolerancia:
                return x_nuevo, puntos, tabla

            x_anterior = x_nuevo
            iteracion += 1

        return None, puntos, tabla

    def falsa_posicion(self, a, b, tolerancia=1e-6, max_iteraciones=100):
        puntos = []
        tabla = []
        iteracion = 1
        c_anterior = a
        
        while iteracion <= max_iteraciones:
            f_a = self.evaluar_funcion(a)
            f_b = self.evaluar_funcion(b)
            
            if f_a * f_b > 0:
                return None, puntos, tabla
            
            if f_b - f_a == 0:
                return None, puntos, tabla
            
            c = b - f_b * (b - a) / (f_b - f_a)
            f_c = self.evaluar_funcion(c)
            
            puntos.append((a, b, c))
            
            error = abs(c - c_anterior)
            tabla.append([f"{iteracion}", f"{a:.6g}", f"{b:.6g}", f"{c:.6g}", f"{f_c:.6g}",f"{error:.6g} %"])
            
            if abs(f_c) < tolerancia or error < tolerancia:
                return c, puntos, tabla
            
            if f_a * f_c < 0:
                b = c
                f_b = f_c
            else:
                a = c
                f_a = f_c
            
            c_anterior = c
            iteracion += 1
        
        return c_anterior, puntos, tabla
    

    def secante(self, x0, x1, tolerancia=1e-6, max_iter=100):
        registro = ""
        puntos_por_raiz = []
        tabla = []  # Lista para almacenar los datos de cada iteración
        
        # Añadir encabezado de la tabla
        #tabla.append(["Iteración", "x0", "x1", "x2", "Error Relativo"])

        for iteracion in range(max_iter):
            f_x0 = self.evaluar_funcion(x0)
            f_x1 = self.evaluar_funcion(x1)

            if f_x1 - f_x0 == 0:
                
                break

            x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
            puntos_por_raiz.append((x0, x1))

            error = self.calcular_error_relativo(x2, x1)

            # Añadir los datos de la iteración a la tabla
            tabla.append([f"{iteracion}", f"{x0:.6g}", f"{x1:.6g}", f"{x2:.6g}", f"{error:.6g} %"])

            if error < tolerancia:
                     
                return x2, puntos_por_raiz, tabla

            x0, x1 = x1, x2

        registro += "\nNo se encontró una raíz en el límite de iteraciones.\n"
        return None, puntos_por_raiz, tabla

    def determinar_dominio(self, expr, variable):
            try:
                # Intentar convertir la expresión a simbólica
                func = sympify(expr)
                
                # Calcular el dominio continuo de la función
                domain = continuous_domain(func, variable, S.Reals)
                return domain
            except Exception:
                return None
