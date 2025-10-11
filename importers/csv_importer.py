"""
matriks/importers/csv_importer.py: Modul tunggal untuk mengimpor data dari CSV.
(Implementasi fitur import CSV wajib).
"""
import csv
import os

class CSVImporter:
    """Kelas yang bertanggung jawab untuk memuat data CSV ke format list bersarang float."""
    
    @staticmethod
    def import_raw_data_from_csv(filepath, column_names, has_header=True):
        """
        Memuat data yang diperlukan dari CSV dan mengonversinya menjadi list bersarang float.
        """
        data_matrix = []
        
        # Tentukan lokasi file CSV (asumsi berada di root project)
        # Kami menggunakan path relatif untuk kompatibilitas yang lebih baik
        script_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_filepath = os.path.join(script_dir, "..", "..", filepath)

        try:
            with open(absolute_filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Mendapatkan indeks kolom
                if has_header:
                    header = next(reader)
                    # Menggunakan strip() untuk menghilangkan spasi/newline pada nama kolom
                    column_indices = [header.index(name.strip()) for name in column_names]
                else:
                    column_indices = list(range(len(column_names)))

                # Membaca data
                for row in reader:
                    processed_row = []
                    for index in column_indices:
                        try:
                            # Mengonversi nilai menjadi float
                            processed_row.append(float(row[index].strip()))
                        except (ValueError, IndexError):
                            # Jika data tidak valid atau hilang, kita isi 0.0
                            processed_row.append(0.0) 
                            
                    if processed_row:
                        data_matrix.append(processed_row)
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"File CSV tidak ditemukan: {absolute_filepath}. Pastikan file ada di root folder.")
        except ValueError as e:
            raise ValueError(f"Error dalam parsing CSV (mungkin nama kolom salah atau data non-numerik): {e}")

        return data_matrix
