# flask_app/pages/routes.py (VERSI FINAL FOKUS REGRESI)

from flask import Blueprint, render_template, request, current_app, redirect, url_for
import os
import pandas as pd 
from io import StringIO 

# Import Modul Low-Level Anda (DIP)
from matriks.matrix import Matrix 
from matriks.importers.csv_importer import CSVImporter
from matriks.regression.linear_regression_model import LinearRegressionModel
# from matriks.exporters.json_exporter import export_to_json # Tidak digunakan lagi

bp = Blueprint("pages", __name__, url_prefix='/')

# Nama Kolom yang sudah divalidasi
FEATURE_COLUMN = "Berat_Kendaraan_kg" 
TARGET_COLUMN = "Konsumsi_Ltr_100km"
CSV_FILENAME = 'konsumsi_bahan_bakar_kendaraan.csv'

@bp.route("/")
def home():
    """Halaman Beranda."""
    return render_template("pages/analysis.html", title="Beranda")

@bp.route("/analysis", methods=["GET", "POST"])
def analyze():
    """Halaman yang menjalankan alur kerja Import, Regresi, dan Interpretasi."""
    
    file_path_root = os.path.join(os.getcwd(), CSV_FILENAME)

    try:
        # 1. Import Data
        raw_data_list = CSVImporter.import_raw_data_from_csv(
            filepath=file_path_root, 
            column_names=[FEATURE_COLUMN, TARGET_COLUMN],
        )
        
        # 2. Persiapan untuk Regresi
        X_data = [[row[0]] for row in raw_data_list] # Feature: Nx1
        y_data = [[row[1]] for row in raw_data_list] # Target: Nx1
        
        feature_matrix = Matrix(X_data)
        target_matrix = Matrix(y_data)
        
        # 3. Latih Model Regresi (Internal menggunakan Inverse & Transpose)
        model = LinearRegressionModel()
        model.fit(feature_matrix, target_matrix)
        weights = model.get_weights() 
        
        # 4. Prediksi untuk Visualisasi
        X_vis = [row[0] for row in X_data] # List fitur X
        y_pred_vis = [model.predict(x) for x in X_vis]
        
        # 5. Interpretasi Hasil (BARU)
        if weights:
            b0 = weights['intercept']
            b1 = weights['slope']
            
            interpretation = (
                f"Model Linear Regression yang dihasilkan adalah: Y = {b0:.4f} + {b1:.4f} * X. "
                f"Ini berarti: "
                f"a) Setiap kenaikan 1 kg pada **Berat Kendaraan** ({FEATURE_COLUMN}), "
                f"diprediksi akan menaikkan **Konsumsi BBM** ({TARGET_COLUMN}) sebesar {b1:.4f} Ltr/100km. "
                f"b) Nilai Intercept ({b0:.4f}) adalah konsumsi BBM prediksi jika berat kendaraan adalah 0 kg. "
                f"Karena bobot kendaraan tidak pernah 0, nilai ini berfungsi sebagai titik awal matematis."
            )
        else:
            interpretation = "Model gagal menghitung bobot."
            
        # 6. Siapkan data untuk Chart.js
        chart_data = {
            'X_data': X_vis, 
            'y_data_actual': [row[0] for row in y_data], 
            'y_data_predicted': y_pred_vis
        }
        
        # 7. Kirim data ke template
        return render_template(
            "pages/analysis.html",
            title="Hasil Analisis",
            feature_name=FEATURE_COLUMN,
            target_name=TARGET_COLUMN,
            weights=weights,
            interpretation=interpretation, # <-- KIRIM INTERPRETASI BARU
            chart_data=chart_data,
            analysis_success=True
        )

    except FileNotFoundError as e:
        return render_template("pages/analysis.html", title="Error", error_message=f"File CSV Error: {e.args[0]}", analysis_success=False)
    except ValueError as e:
        return render_template("pages/analysis.html", title="Error", error_message=f"Kesalahan Validasi Data: {e}", analysis_success=False)
    except Exception as e:
        return render_template("pages/analysis.html", title="Error", error_message=f"Kesalahan Analisis: Terjadi error pada aljabar matriks atau model: {e}", analysis_success=False)