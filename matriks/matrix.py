"""
matriks/matrix.py: Kelas inti untuk representasi dan manipulasi matriks.
Menerapkan operasi intrinsik (Unary) seperti transpose dan inverse.
"""

class Matrix:
    """
    Merepresentasikan objek matriks (nested list/list bersarang) 
    dan menyediakan fungsionalitas dasar matriks, termasuk transpose dan inverse.
    """
    def __init__(self, data_list):
        # Memastikan input adalah struktur yang valid
        if not isinstance(data_list, list) or not all(isinstance(row, list) for row in data_list):
            raise ValueError("Data matriks harus berupa list bersarang.")

        self.data = data_list
        self.row_count = len(data_list)
        self.column_count = len(data_list[0]) if self.row_count > 0 else 0

        # Validasi konsistensi kolom
        if not all(len(row) == self.column_count for row in data_list):
            raise ValueError("Semua baris dalam matriks harus memiliki panjang kolom yang sama.")

    def __str__(self):
        """Representasi string yang mudah dibaca."""
        matrix_string = "[\n"
        for row in self.data:
            matrix_string += "  [" + ", ".join(f"{x:.4f}" for x in row) + "],\n"
        return matrix_string.rstrip(',\n') + "\n]"

    def get_data(self):
        """Mengembalikan data matriks."""
        return self.data

    def get_dimensions(self):
        """Mengembalikan jumlah baris dan kolom."""
        return self.row_count, self.column_count

    # FITUR WAJIB: Transpose (Operasi Unary)
    def transpose(self):
        """Melakukan operasi transpose."""
        if self.row_count == 0 or self.column_count == 0:
            return Matrix([[]])

        transposed_data = []
        for j in range(self.column_count):
            new_row = []
            for i in range(self.row_count):
                new_row.append(self.data[i][j])
            transposed_data.append(new_row)

        return Matrix(transposed_data)

    # FITUR WAJIB: Inverse (Operasi Unary) - Menggunakan metode Gauss-Jordan
    def inverse(self):
        """Menghitung invers matriks persegi menggunakan Gauss-Jordan."""
        if self.row_count != self.column_count:
            raise ValueError("Invers hanya dapat dihitung untuk matriks persegi.")

        size = self.row_count

        # Membuat matriks augmented [A | I]
        augmented_data = [row[:] for row in self.data]
        for i in range(size):
            identity_row = [0.0] * size
            identity_row[i] = 1.0
            augmented_data[i].extend(identity_row)

        # Proses Eliminasi Gauss-Jordan
        for i in range(size):
            # Normalisasi pivot (membuat diagonal menjadi 1)
            pivot = augmented_data[i][i]
            if abs(pivot) < 1e-9: 
                raise ValueError("Matriks ini singular atau hampir singular, tidak memiliki invers.")
            
            divisor = pivot
            for j in range(2 * size):
                augmented_data[i][j] /= divisor
            
            # Eliminasi (membuat elemen lain di kolom menjadi 0)
            for k in range(size):
                if k != i:
                    factor = augmented_data[k][i]
                    for j in range(2 * size):
                        augmented_data[k][j] -= factor * augmented_data[i][j]

        # Mengekstrak matriks invers
        inverse_data = [row[size:] for row in augmented_data]
        return Matrix(inverse_data)

