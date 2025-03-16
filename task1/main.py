class Matrix2D:
    def __init__(self):
        self.matrix = [[0, 0], [0, 0]]

    def input_from_keyboard(self):
        print("Введіть 4 числа для матриці 2x2 (в двух рядках):")
        for i in range(2):
            row = input(f"Рядок {i+1} (2 числа через пробіл): ").split()
            self.matrix[i] = [float(x) for x in row]

    def input_from_file(self, line):
        numbers = [float(x) for x in line.split()]
        self.matrix = [[numbers[0], numbers[1]], [numbers[2], numbers[3]]]

    def output_to_screen(self):
        for row in self.matrix:
            print(row)

    def output_to_file(self, file):
        for row in self.matrix:
            file.write(f"{row[0]} {row[1]}\n")

    def determinant(self):
        return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]

    def is_degenerate(self):
        return abs(self.determinant()) < 1e-10

class Vector2D:
    def __init__(self):
        self.vector = [0, 0]

    def input_from_file(self, line):
        self.vector = [float(x) for x in line.split()]

    def output_to_screen(self):
        print(f"Вектор: {self.vector}")

class Solver:
    def __init__(self, matrix, vector):
        self.matrix = matrix
        self.vector = vector

    def solve_cramer(self):
        det = self.matrix.determinant()
        if self.matrix.is_degenerate():
            return "Система не має єдиного розв’язку (визначник = 0)"

        # матриця для x1
        matrix_x1 = Matrix2D()
        matrix_x1.matrix = [[self.vector.vector[0], self.matrix.matrix[0][1]],
                           [self.vector.vector[1], self.matrix.matrix[1][1]]]
        det_x1 = matrix_x1.determinant()

        # матриця для x2
        matrix_x2 = Matrix2D()
        matrix_x2.matrix = [[self.matrix.matrix[0][0], self.vector.vector[0]],
                           [self.matrix.matrix[1][0], self.vector.vector[1]]]
        det_x2 = matrix_x2.determinant()

        x1 = det_x1 / det
        x2 = det_x2 / det
        return f"x1 = {x1}, x2 = {x2}"

# MAIN
def main():
    with open("matrix_coefficients.txt", "r") as matrix_file, \
         open("rhs_values.txt", "r") as rhs_file, \
         open("output.txt", "w") as output_file:

        matrix_lines = matrix_file.readlines()
        rhs_lines = rhs_file.readlines()

        for i, (matrix_line, rhs_line) in enumerate(zip(matrix_lines, rhs_lines), 1):
          
            matrix = Matrix2D()
            vector = Vector2D()

            matrix.input_from_file(matrix_line.strip())
            vector.input_from_file(rhs_line.strip())

            output_file.write(f"\nСистема {i}:\nМатриця:\n")
            matrix.output_to_file(output_file)
            output_file.write("Права частина:\n")
            vector.output_to_screen()
            output_file.write(f"{vector.vector[0]} {vector.vector[1]}\n")

            solver = Solver(matrix, vector)
            result = solver.solve_cramer()

            print(f"\nСистема {i}:")
            matrix.output_to_screen()
            vector.output_to_screen()
            print(result)
            output_file.write(f"Розв’язок: {result}\n")

if __name__ == "__main__":
    main()
