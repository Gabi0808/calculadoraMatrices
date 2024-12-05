class Formateador:
    @staticmethod
    def format_expression(terms):
        expr = ""
        for idx, term in enumerate(terms):
            if idx == 0:
                expr += str(term)
            else:
                if term >= 0:
                    expr += f" + {term}"
                else:
                    expr += f" - {abs(term)}"
        return expr

    @staticmethod
    def box_vector(vector, title=""):
        number_strings = [str(num) for num in vector]
        max_num_length = max(len(s) for s in number_strings)
        max_line_length = max(max_num_length, len(title)) + 2

        result = f"┌{'─' * max_line_length}┐\n"
        if title:
            result += f"│ {title.center(max_line_length - 2)} │\n"
            result += f"├{'─' * max_line_length}┤\n"

        for num_str in number_strings:
            result += f"│ {num_str.rjust(max_line_length - 2)} │\n"

        result += f"└{'─' * max_line_length}┘\n"
        return result

    @staticmethod
    def box_vector_horizontal(vector, title=""):
        number_strings = [str(num) for num in vector]
        max_num_length = max(len(s) for s in number_strings)
        total_width = len(vector) * (max_num_length + 1) + (len(vector)+1)

        result = f"┌{'─' * total_width}┐\n"
        if title:
            centered_title = title.center(total_width)
            result += f"│{centered_title}│\n"
            result += f"├{'─' * total_width}┤\n"

        row_str = " ".join(f"{num.rjust(max_num_length)} " for num in number_strings)
        result += f"│ {row_str} │\n"
        result += f"└{'─' * total_width}┘\n"
        return result
    
    @staticmethod
    def box_matrix_and_vectors(matrix, vector1, vector2, matrix_title="", vector1_title="", vector2_title=""):
        def colorize_text(text, color):
            return f'<span style="color: {color};">{text}</span>'

        def box_matrix(matrix, title="", colors=None):
            matrix_str = [[str(num) for num in row] for row in matrix]
            max_num_length = max(len(num) for row in matrix_str for num in row)
            title_length = len(title)
            total_width = max(len(matrix[0]) * (max_num_length + 2) + 1, title_length + 2)

            result = f"┌{'─' * total_width}┐\n"
            if title:
                centered_title = title.center(total_width)
                result += f"│{centered_title}│\n"
                result += f"├{'─' * total_width}┤\n"

            for row in matrix_str:
                row_str = "  ".join(colorize_text(num.center(max_num_length), colors[j % len(colors)]) for j, num in enumerate(row))
                row_str = row_str.center(total_width - 2)  # Centrar la fila dentro del ancho total
                result += f"│ {row_str}  │\n"

            result += f"└{'─' * total_width}┘\n"
            return result

        def box_vector(vector, title="", color="black"):
            vector_str = [str(num) for num in vector]
            max_num_length = max(len(num) for num in vector_str)
            title_length = len(title)
            total_width = max(max_num_length + 2, title_length + 2)

            result = f"┌{'─' * total_width}┐\n"
            if title:
                centered_title = title.center(total_width)
                result += f"│{centered_title}│\n"
                result += f"├{'─' * total_width}┤\n"

            for num in vector_str:
                centered_num = colorize_text(num.center(max_num_length), color).center(total_width - 2)
                result += f"│ {centered_num} │\n"

            result += f"└{'─' * total_width}┘\n"
            return result

        # Definir colores
        column_colors = ["red", "green", "blue", "orange"]  # Colores para las columnas
        vector_color = "purple"

        # Crear cajas individuales con colores
        matrix_box = box_matrix(matrix, matrix_title, colors=column_colors)
        vector1_box = box_vector(vector1, vector1_title, color=vector_color)
        vector2_box = box_vector(vector2, vector2_title, color='black')

        # Separar las líneas de cada caja para combinarlas
        matrix_lines = matrix_box.split("\n")
        vector1_lines = vector1_box.split("\n")
        vector2_lines = vector2_box.split("\n")

        # Ajustar las longitudes para que todas las cajas tengan el mismo número de líneas
        max_lines = max(len(matrix_lines), len(vector1_lines), len(vector2_lines))
        matrix_lines += [" " * len(matrix_lines[0])] * (max_lines - len(matrix_lines))
        vector1_lines += [" " * len(vector1_lines[0])] * (max_lines - len(vector1_lines))
        vector2_lines += [" " * len(vector2_lines[0])] * (max_lines - len(vector2_lines))

        # Construir cada línea combinando las cajas
        header=f" Matriz\tVector  Resultado\n"
        combined_lines = [
            f"{matrix_line}   {vector1_line}   {vector2_line}"
            for matrix_line, vector1_line, vector2_line in zip(matrix_lines, vector1_lines, vector2_lines)
        ]

        # Devolver la combinación completa como HTML para QTextEdit
        return "<pre>" + header +"\n".join(combined_lines) + "</pre>"

class MatrizHelper:
    @staticmethod
    def box_matrix(matrix, title=""):

        matrix_str = [[str(num) for num in row] for row in matrix]
        
        max_num_length = max(len(num) for row in matrix_str for num in row)

        total_width = len(matrix[0]) * (max_num_length + 1) + (len(matrix[0])+1)

        result = f"┌{'─' * total_width}┐\n"
        if title:
            centered_title = title.center(total_width)
            result += f"│{centered_title}│\n"
            result += f"├{'─' * total_width}┤\n"

        for row in matrix_str:
            row_str = " ".join(f"{num.rjust(max_num_length)} " for num in row)
            result += f"│ {row_str} │\n"

        result += f"└{'─' * total_width}┘\n"
        
        return result

class GestorPasos:
    def __init__(self):
        self.pasos = []

    def agregar_paso(self, descripcion, vector=None, matriz=None):
        self.pasos.append(descripcion)
        if vector is not None:
            self.pasos.append(vector)
        if matriz is not None:
            self.pasos.append(matriz.mostrar())

    def mostrar_pasos(self):
        return "\n".join(self.pasos)


