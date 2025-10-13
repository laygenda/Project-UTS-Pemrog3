"""matriks/validators/is_square.py: Validasi matriks persegi."""
from ..matrix import Matrix

def is_square(matrix_object: Matrix):
    """Mengembalikan True jika matriks memiliki jumlah baris = jumlah kolom."""
    rows, cols = matrix_object.get_dimensions()
    return rows == cols
