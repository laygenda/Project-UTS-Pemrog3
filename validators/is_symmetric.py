"""matriks/validators/is_symmetric.py: Validasi matriks simetris."""
from ..matrix import Matrix
from .is_square import is_square

def is_symmetric(matrix_object: Matrix, tolerance=1e-9):
    """Mengembalikan True jika matriks simetris."""
    if not is_square(matrix_object):
        return False
        
    data = matrix_object.get_data()
    size = matrix_object.row_count
    
    for i in range(size):
        for j in range(i + 1, size):
            if abs(data[i][j] - data[j][i]) > tolerance:
                return False
    return True
