"""matriks/validators/is_identity.py: Validasi matriks identitas."""
from ..matrix import Matrix
from .is_square import is_square

def is_identity(matrix_object: Matrix, tolerance=1e-9):
    """Mengembalikan True jika matriks identitas."""
    if not is_square(matrix_object):
        return False
        
    data = matrix_object.get_data()
    size = matrix_object.row_count
    
    for i in range(size):
        for j in range(size):
            target = 1.0 if i == j else 0.0
            if abs(data[i][j] - target) > tolerance:
                return False
    return True
