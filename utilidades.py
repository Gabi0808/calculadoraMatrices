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


