"""
matriks/sparsematrix.py: Implementasi Matriks Jarang (Sparse Matrix) yang efisien.

Kelas ini mewarisi dari Matrix untuk membuktikan Liskov Substitution Principle (LSP)
dan Open/Closed Principle (OCP).
"""
from matriks.matrix import Matrix
from collections import defaultdict

class SparseMatrix(Matrix):
    """
    Merepresentasikan matriks di mana sebagian besar elemennya adalah nol.
    Data disimpan menggunakan format Dictionary of Keys (DOK): {(baris, kolom): nilai}.
    """
    def __init__(self, data_list):
        # Inisialisasi placeholder superclass
        super().__init__([[0]])

        # Mengidentifikasi dimensi dari data_list yang diberikan
        self.row_count = len(data_list)
        self.column_count = len(data_list[0]) if self.row_count > 0 else 0

        # Penyimpanan data yang efisien (DOK format)
        self._sparse_data = {}
        self._initialize_sparse_data(data_list)

    def _initialize_sparse_data(self, data_list):
        """Mengisi data sparse hanya dengan elemen yang bukan nol."""
        for i in range(self.row_count):
            for j in range(self.column_count):
                value = data_list[i][j]
                # Angka yang sangat kecil dianggap nol (untuk menghindari floating point noise)
                if abs(value) > 1e-9:
                    self._sparse_data[(i, j)] = value

    # LSP Bukti: Metode get_data() HARUS mengembalikan data dalam format Dense
    # agar MatrixMultiplier (kode lama) dapat bekerja tanpa diubah.
    def get_data(self):
        """Mengembalikan representasi data matriks sebagai list bersarang (Dense format)."""
        dense_data = [[0.0] * self.column_count for _ in range(self.row_count)]

        for (i, j), value in self._sparse_data.items():
            if i < self.row_count and j < self.column_count:
                dense_data[i][j] = value

        return dense_data

    # Menimpa (override) metode transpose untuk mengembalikan objek SparseMatrix baru
    def transpose(self):
        """Melakukan transpose Sparse Matrix."""
        # Menghitung transpose secara internal (menukar i dan j)
        new_sparse_data = {}
        for (i, j), value in self._sparse_data.items():
            new_sparse_data[(j, i)] = value

        # Mengonversi hasil transpose ke Dense lalu ke SparseMatrix baru
        # Ini adalah cara sederhana untuk memastikan konsistensi dimensi

       # transposed_dense_data = super().transpose().get_data()
       # return SparseMatrix(transposed_dense_data)

       # ini menyebabkan bug kecil, yang menyebabkan eror saat mencoba mendemontrasikan 
       # sparsematrix transpose di main.py

       # hal itu karena Memanggil super().transpose() yang mengembalikan matrx penuh
#	yang sudah benar transposenya, kemudian program mencoba untuk mengembalikan
 #      sparsematrix dengan data dense tersebut, yang menimbulkan masalah saat
  #     mengkonstruksi objek sparse yang baru, terutama terkait dimensi baru (Kolom A
#	menjadi baris B

       # di bawah ini adalah perbaikan kode yang menyebabkan bug
       # Membuat SparseMatrix baru dengan data ter-transpose
        new_matrix = SparseMatrix([[0]])
        new_matrix._sparse_data = new_sparse_data
    
        # Menukar ukuran baris dan kolom
        new_matrix.row_count = self.column_count
        new_matrix.column_count = self.row_count

        return new_matrix

    def __str__(self):
        """Representasi string untuk output yang mudah dibaca."""
        # Memberi tahu pengguna bahwa ini adalah SparseMatrix
        matrix_string = f"SparseMatrix (Hanya menyimpan {len(self._sparse_data)} elemen non-nol) [\n"
        dense_data = self.get_data()
        for row in dense_data:
            matrix_string += "  [" + ", ".join(f"{x:.4f}" for x in row) + "],\n"
        matrix_string = matrix_string.rstrip(',\n') + "\n]"
        return matrix_string

