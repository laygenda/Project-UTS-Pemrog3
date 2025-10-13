"""
matriks/importers/csv_importer.py: Modul tunggal untuk mengimpor data dari CSV.
"""
import csv
import os
import sys

class CSVImporter:
    """Kelas yang bertanggung jawab untuk memuat data CSV ke format list bersarang float."""
    
    @staticmethod
    def import_raw_data_from_csv(filepath, column_names, has_header=True, is_relative_to_main=False):
        """
        Memuat data yang diperlukan dari CSV dan mengonversinya menjadi list bersarang float.

        Args:
            filepath (str): Nama file CSV (e.g., 'data.csv').
            column_names (list): List nama kolom yang akan diambil.
            has_header (bool): Apakah file memiliki header.
            is_relative_to_main (bool): Jika True, path relatif terhadap direktori yang 
                                        menjalankan main.py (yaitu /matriks/).
        """
        
        # if is_relative_to_main:
        #     # Jika dijalankan dari main.py di folder /matriks/, path CSV ada di sana.
        #     absolute_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", filepath))
        # else:
        #     # Jika dijalankan dari Flask (root project), path CSV ada di root.
        #     # Kita asumsikan Flask dijalankan dari /Project-UTS-PM3/, dan CSV ada di /Project-UTS-PM3/
        #     #absolute_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", filepath))

        # --- LOGIKA PATH TEPAT UNTUK FLASK ---
        if is_relative_to_main:
            # Kasus 1: Dijalankan dari main.py (Legacy/Debug)
            # Path relatif terhadap matriks/importers/
            absolute_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", filepath))
        else:
            # Kasus 2: Dijalankan oleh Flask/Orchestrator
            # os.getcwd() adalah *root* proyek tempat 'flask run' dijalankan.
            # Ini adalah path yang paling andal.
            absolute_filepath = os.path.join(os.getcwd(), filepath)

        data_matrix = []
        
        try:
            # # Cek di mana file tersebut benar-benar ada
            # if not os.path.exists(absolute_filepath):
            #      # Jika tidak ditemukan di path yang dihitung, coba di current working directory
            #      absolute_filepath = filepath
            #      if not os.path.exists(absolute_filepath):
            #          raise FileNotFoundError(f"File data tidak ditemukan di: {filepath} atau {absolute_filepath}")
            if not os.path.exists(absolute_filepath):
                 raise FileNotFoundError(
                    f"File data tidak ditemukan di: {absolute_filepath}"
                 )

            with open(absolute_filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Mendapatkan indeks kolom
                if has_header:
                    # ... (logika header tetap sama) ...
                    header = next(reader)
                    if not all(name.strip() in [h.strip() for h in header] for name in column_names):
                        raise ValueError(f"Kolom yang diminta {column_names} tidak ditemukan di header: {header}")
                        
                    column_indices = [[h.strip() for h in header].index(name.strip()) for name in column_names]
                else:
                    column_indices = list(range(len(column_names)))

                # Membaca data
                for row in reader:
                    processed_row = []
                    for index in column_indices:
                        try:
                            processed_row.append(float(row[index].strip()))
                        except (ValueError, IndexError):
                            # Jika data tidak valid atau hilang
                            processed_row.append(0.0) 
                            
                    if processed_row:
                        data_matrix.append(processed_row)
                        
        except FileNotFoundError as e:
            # Tampilkan pesan error yang menunjukkan path yang gagal
            raise FileNotFoundError(f"File CSV tidak ditemukan: {absolute_filepath}")
        except ValueError as e:
            raise ValueError(f"Error dalam parsing CSV: {e}")

        return data_matrix
