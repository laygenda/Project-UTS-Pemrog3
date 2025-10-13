"""
matriks/regression/linear_regression_model.py: Implementasi Algoritma Regresi Linear.
(Memenuhi fitur wajib Algoritma Regresi Linear).
"""
from ..matrix import Matrix
from ..operations.multiplier import MatrixMultiplier

class LinearRegressionModel:
    """
    Model Regresi Linear Sederhana menggunakan Persamaan Normal: W = (X^T X)^-1 X^T Y.
    """
    def __init__(self):
        self.weights = None # Matriks bobot (b0: Intercept, b1: Slope)

    def fit(self, feature_matrix: Matrix, target_matrix: Matrix):
        """
        Melatih model Regresi Linear.
        """
        # 1. Feature Engineering: Menambahkan kolom 1 untuk Intercept (X_augmented = [1 | X])
        data_x = feature_matrix.get_data()
        augmented_x_data = [[1.0] + row for row in data_x]
        x_augmented = Matrix(augmented_x_data)
        
        # 2. Transpose X: X_T = X_augmented.transpose()
        x_transpose = x_augmented.transpose()
        
        # 3. Hitung X_T_X = X_T * X 
        x_transpose_x = MatrixMultiplier.multiply(x_transpose, x_augmented)
        
        # 4. Hitung X_T_X_inv = (X_T * X)^-1 
        try:
            x_transpose_x_inverse = x_transpose_x.inverse()
        except ValueError as e:
            raise RuntimeError(f"Gagal menghitung invers (matriks singular): {e}")
        
        # 5. Hitung X_T_Y = X_T * Y
        x_transpose_y = MatrixMultiplier.multiply(x_transpose, target_matrix)
        
        # 6. Hitung Weights: W = X_T_X_inv * X_T_Y
        self.weights = MatrixMultiplier.multiply(x_transpose_x_inverse, x_transpose_y)
        
        print("Pelatihan Model Regresi Linear Selesai.")
        
    def predict(self, feature_value: float):
        """
        Membuat prediksi tunggal: Y_pred = b0 + b1 * X
        """
        if self.weights is None:
            raise Exception("Model belum dilatih. Panggil metode fit() terlebih dahulu.")
        
        # W = [[b0], [b1]]
        intercept = self.weights.get_data()[0][0] 
        slope = self.weights.get_data()[1][0]     
        
        prediction = intercept + slope * feature_value
        return prediction

    def get_weights(self):
        """Mengembalikan nilai bobot yang telah diprediksi."""
        if self.weights is None:
            return None
        
        return {
            "intercept": self.weights.get_data()[0][0],
            "slope": self.weights.get_data()[1][0]
        }
