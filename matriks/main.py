"""
matriks/main.py: Demonstrasi Penggunaan Modul Matriks, CSV Importer, dan Regresi Linear.
"""
# Menggunakan ABSOLUTE IMPORT untuk mengatasi masalah "no known parent package"
# Karena main.py dijalankan sebagai skrip utama.
# Import dari root package 'matriks'
from matriks.matrix import Matrix
from matriks.sparsematrix import SparseMatrix 
from matriks.importers.csv_importer import CSVImporter
from matriks.regression.linear_regression_model import LinearRegressionModel
from matriks.operations.multiplier import MatrixMultiplier
import os 
import sys


def run_analysis_demonstration():
    """
    Mengelola alur kerja analisis Regresi Linear dan mendemonstrasikan fitur matriks.
    """
    print("=================================================================")
    print("      DEMO PROJECT MATRIX: PREDIKSI KONSUMSI BAHAN BAKAR         ")
    print("=================================================================")

    # Asumsi file 'konsumsi bahan bakar kendaraan.csv' berada di folder 'matriks'
    csv_filename = "konsumsi bahan bakar kendaraan.csv" 
    
    # --- Bagian 1: Import Data CSV dan Pelatihan Regresi ---
    try:
        print(f"\n[1] Memuat data dari '{csv_filename}' (Import CSV)...")
        
        # Kolom Fitur (X): Berat_Kendaraan_kg
        # Path disesuaikan agar mencari file di direktori saat ini
        feature_data = CSVImporter.import_raw_data_from_csv(
            filepath=csv_filename, 
            column_names=['Berat_Kendaraan_kg'],
            is_relative_to_main=True # Tambahkan parameter baru
        )
        # Kolom Target (Y): Konsumsi_Ltr_100km
        target_data = CSVImporter.import_raw_data_from_csv(
            filepath=csv_filename, 
            column_names=['Konsumsi_Ltr_100km'],
            is_relative_to_main=True # Tambahkan parameter baru
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
        matrix_c_data = [[1.0], [2.0], [3.0]]
        matrix_c = Matrix(matrix_c_data)

        print("\n-> Bukti LSP/OCP: Perkalian SparseMatrix dengan Matrix C (3x1)")
        result_matrix = MatrixMultiplier.multiply(sparse_matrix_b, matrix_c)

        print("   -> Hasil Perkalian (SparseMatrix * Matrix):")
        print(result_matrix)
        
        transposed_sparse = sparse_matrix_b.transpose()
        print("\n   -> SparseMatrix Transpose:")
        print(transposed_sparse)


    except Exception as e:
        print(f"   -> Gagal menjalankan LSP/OCP test: {e}")

    # --- Bagian 4: Demonstrasi Operasi Matriks Wajib ---
    print("\n[5] Demonstrasi Operasi Matriks Wajib (Transpose & Inverse):")
    
    verify_data = [[1.0, 2.0], [3.0, 4.0]]
    verify_matrix = Matrix(verify_data)
    
    print("\n   - Matriks Awal (2x2):")
    print(verify_matrix)

    transposed_matrix = verify_matrix.transpose()
    print("\n   - Matriks Transpose (A^T):")
    print(transposed_matrix)

    try:
        inverse_matrix = verify_matrix.inverse()
        print("\n   - Matriks Inverse (A^-1):")
        print(inverse_matrix)
    except ValueError as e:
        print(f"\n   - Gagal menghitung invers matriks demo: {e}")


if __name__ == "__main__":
    # Penting: Saat menjalankan main.py sebagai skrip, kita perlu memastikan 
    # Python dapat menemukan package 'matriks' di current working directory.
    if os.getcwd().split(os.sep)[-1] == 'matriks':
        # Jika dijalankan dari dalam folder 'matriks', tambahkan parent directory ke path
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
    run_analysis_demonstration()

