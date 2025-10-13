"""matriks/exporters/json_exporter.py: Modul untuk mengekspor matriks ke format JSON."""
import json
from ..matrix import Matrix

def export_to_json(matrix_object: Matrix, filepath: str):
    """Mengekspor data matriks ke file JSON."""
    data_to_export = {
        "rows": matrix_object.row_count,
        "columns": matrix_object.column_count,
        "data": matrix_object.get_data()
    }
    with open(filepath, 'w') as file:
        json.dump(data_to_export, file, indent=4)
    print(f"Matriks berhasil diekspor ke {filepath}")
