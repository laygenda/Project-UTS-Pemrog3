"""
matriks/operations/multiplier.py: Modul untuk operasi perkalian matriks (A * B).
(Memenuhi SRP: hanya bertanggung jawab pada perkalian biner.)
"""
from ..matrix import Matrix

class MatrixMultiplier:
    """Kelas statis untuk mengalikan dua matriks."""
    
    @staticmethod
    def multiply(matrix_a: Matrix, matrix_b: Matrix):
        """Melakukan perkalian matriks."""
        rows_a, cols_a = matrix_a.get_dimensions()
        rows_b, cols_b = matrix_b.get_dimensions()

        if cols_a != rows_b:
            raise ValueError(
                "Tidak dapat mengalikan. Jumlah kolom matriks pertama "
                "harus sama dengan jumlah baris matriks kedua (A * B)."
            )

        data_a = matrix_a.get_data()
        data_b = matrix_b.get_data()
        
        result_data = [[0.0] * cols_b for _ in range(rows_a)]

        for i in range(rows_a): 
            for j in range(cols_b): 
                sum_of_products = 0.0
                for k in range(cols_a): 
                    # Inti perkalian: A[i][k] * B[k][j]
                    sum_of_products += data_a[i][k] * data_b[k][j]
                result_data[i][j] = sum_of_products

        return Matrix(result_data)

