"""matriks/exporters/csv_exporter.py: Modul untuk mengekspor matriks ke format CSV."""
import csv
from ..matrix import Matrix

def export_to_csv(matrix_object: Matrix, filepath: str):
    """Mengekspor data matriks ke file CSV."""
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(matrix_object.get_data())
    print(f"Matriks berhasil diekspor ke {filepath}")
