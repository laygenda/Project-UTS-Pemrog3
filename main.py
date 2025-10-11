"""
matriks/main.py: Demonstrasi Penggunaan Modul Matriks, CSV Importer, dan Regresi Linear.

File ini berada di root folder 'matriks/'
"""
from matrix import Matrix
from sparsematrix import SparseMatrix 
from importers.csv_importer import CSVImporter
from regression.linear_regression_model import LinearRegressionModel
from operations.multiplier import MatrixMultiplier
import os 
import sys

# Tambahkan path package matriks agar bisa diimport dengan benar
# Ini diperlukan karena main.py berada di dalam package matriks
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_analysis_demonstration():
    """
    Mengelola alur kerja analisis Regresi Linear dan mendemonstrasikan fitur matriks.
    """
    print("=================================================================")
    print("      DEMO PROJECT MATRIX: PREDIKSI KONSUMSI BAHAN BAKAR         ")
    print("=================================================================")

    # Asumsi file 'konsumsi bahan bakar kendaraan.csv' berada di root direktori project
    csv_filename = "konsumsi bahan bakar kendaraan.csv" 
    
    # --- Bagian 1: Import Data CSV dan Pelatihan Regresi ---
    try:
        print(f"\n[1] Memuat data dari '{csv_filename}' (Import CSV)...")
        
        # Kolom Fitur (X): Berat_Kendaraan_kg
        feature_data = CSVImporter.import_raw_data_from_csv(
            filepath=csv_filename, 
            column_names=['Berat_Kendaraan_kg']
        )
        # Kolom Target (Y): Konsumsi_Ltr_100km
        target_data = CSVImporter.import_raw_data_from_csv(
            filepath=csv_filename, 
            column_names=['Konsumsi_Ltr_100km']
        )
        
        feature_matrix = Matrix(feature_data)
        target_matrix = Matrix(target_data)
        
        print(f"-> Data berhasil dimuat: {feature_matrix.row_count} sampel.")

        print("\n[2] Memulai Pelatihan Model Regresi Linear (Menggunakan Transpose, Perkalian, Inverse Matriks)...")
        model = LinearRegressionModel()
        model.fit(feature_matrix, target_matrix)
        weights = model.get_weights()
        
        if weights:
            print("\n-> Hasil Regresi Linear (Bobot Model):")
            print(f"   Intercept (b0): {weights['intercept']:.6f}")
            print(f"   Slope (b1)    : {weights['slope']:.6f}")
        
    except Exception as e:
        print(f"Error saat memproses regresi: {e}")
        return

    # --- Bagian 3: Demonstrasi LSP dan OCP dengan SparseMatrix ---
    print("\n=================================================================")
    print("      DEMO OCP & LSP: MENGGUNAKAN SPARSE MATRIX                  ")
    print("=================================================================")

    sparse_data = [
        [10.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 5.0, 0.0]
    ]

    sparse_matrix_b = SparseMatrix(sparse_data)
    
    print("\n-> Matriks Jarang (SparseMatrix) yang dibuat:")
    print(sparse_matrix_b)
    
    try:
        # Matriks C (3x1) untuk perkalian
        matrix_c_data = [[1.0], [2.0], [3.0]]
        matrix_c = Matrix(matrix_c_data)

        print("\n-> Bukti LSP/OCP: Perkalian SparseMatrix dengan Matrix C (3x1)")
        # MatrixMultiplier hanya memanggil sparse_matrix_b.get_data().
        # Karena SparseMatrix mengimplementasikan get_data() dengan benar (LSP), operasi berhasil.
        result_matrix = MatrixMultiplier.multiply(sparse_matrix_b, matrix_c)

        print("   -> Hasil Perkalian (SparseMatrix * Matrix):")
        print(result_matrix)
        
        # Test Transpose Sparse Matrix
        transposed_sparse = sparse_matrix_b.transpose()
        print("\n   -> SparseMatrix Transpose:")
        print(transposed_sparse)


    except Exception as e:
        print(f"   -> Gagal menjalankan LSP/OCP test: {e}")


if __name__ == "__main__":
    run_analysis_demonstration()
