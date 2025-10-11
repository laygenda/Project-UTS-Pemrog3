"""matriks/operations/adder.py: Modul untuk operasi penjumlahan matriks (A + B)."""
from ..matrix import Matrix

class MatrixAdder:
    @staticmethod
    def add(matrix_a: Matrix, matrix_b: Matrix):
        rows_a, cols_a = matrix_a.get_dimensions()
        rows_b, cols_b = matrix_b.get_dimensions()

        if rows_a != rows_b or cols_a != cols_b:
            raise ValueError("Matriks harus memiliki dimensi yang sama untuk penjumlahan.")

        data_a = matrix_a.get_data()
        data_b = matrix_b.get_data()
        result_data = [[data_a[i][j] + data_b[i][j] for j in range(cols_a)] for i in range(rows_a)]

        return Matrix(result_data)

