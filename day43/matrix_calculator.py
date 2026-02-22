# Calculadora e matrices
# dos matrices
# Suma
# resta
# multiplicacion
# determinante
# transposicion
# inversa

# manejo de entradas invalidas
import numpy as np
def get_matrix_input():
    while True:
        try:
            rows = int(input("Number of rows: "))
            cols = int(input("Number of columns: "))
            if rows <= 0 or cols <= 0:
                print("Please enter positive integers for rows and columns.")
                continue
            matrix = []
            for i in range(rows):
                row_input = input(f"Enter the elements of row {i + 1} separated by spaces: ")
                row = list(map(float, row_input.split()))
                if len(row) != cols:
                    print(f"Please enter exactly {cols} elements for row {i + 1}.")
                    break
                matrix.append(row)
            else:
                return matrix
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{elem:.2f}" for elem in row))

def add_matrices(matrix_a, matrix_b):
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        print("Error: Matrices must have the same dimensions for addition.")
        return None
    return np.add(matrix_a, matrix_b).tolist()

def subtract_matrices(matrix_a, matrix_b):
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        print("Error: Matrices must have the same dimensions for subtraction.")
        return None
    return np.subtract(matrix_a, matrix_b).tolist()


def multiply_matrices(matrix_a, matrix_b):
    if len(matrix_a[0]) != len(matrix_b):
        print("Error: Number of columns in the first matrix must equal the number of rows in the second matrix for multiplication.")
        return None
    return np.dot(matrix_a, matrix_b).tolist()

def determinant(matrix):
    if len(matrix) != len(matrix[0]):
        print("Error: Matrix must be square to calculate determinant.")
        return None
    return np.linalg.det(matrix)

def transpose(matrix):
    return np.transpose(matrix).tolist()

def inverse(matrix):
    if len(matrix) != len(matrix[0]):
        print("Error: Matrix must be square to calculate inverse.")
        return None
    try:
        return np.linalg.inv(matrix).tolist()
    except np.linalg.LinAlgError:
        print("Error: Matrix is singular and cannot be inverted.")
        return None

def main():
    print("Matrix Calculator")
    print("Enter the first matrix:")
    matrix_a = get_matrix_input()
    print("Enter the second matrix:")
    matrix_b = get_matrix_input()

    print("\nMatrix A:")
    print_matrix(matrix_a)
    print("\nMatrix B:")
    print_matrix(matrix_b)

    print("\nSum of A and B:")
    sum_result = add_matrices(matrix_a, matrix_b)
    if sum_result is not None:
        print_matrix(sum_result)

    print("\nDifference of A and B:")
    diff_result = subtract_matrices(matrix_a, matrix_b)
    if diff_result is not None:
        print_matrix(diff_result)

    print("\nProduct of A and B:")
    prod_result = multiply_matrices(matrix_a, matrix_b)
    if prod_result is not None:
        print_matrix(prod_result)

    print("\nDeterminant of A:")
    det_a = determinant(matrix_a)
    if det_a is not None:
        print(f"{det_a:.2f}")

    print("\nDeterminant of B:")
    det_b = determinant(matrix_b)
    if det_b is not None:
        print(f"{det_b:.2f}")

    print("\nTranspose of A:")
    trans_a = transpose(matrix_a)
    print_matrix(trans_a)
    print("\nTranspose of B:")
    trans_b = transpose(matrix_b)
    print_matrix(trans_b)
    print("\nInverse of A:")
    inv_a = inverse(matrix_a)
    if inv_a is not None:
        print_matrix(inv_a)
    print("\nInverse of B:")
    inv_b = inverse(matrix_b)
    if inv_b is not None:
        print_matrix(inv_b)
        
if __name__ == "__main__":
    main()