# flask_app/pages/routes.py (VERSI FINAL + FIX HOME VARS)

from flask import Blueprint, render_template, request, current_app, redirect, url_for
import os
import math # Diperlukan untuk sqrt()
# Import Modul Low-Level Anda (DIP)
from matriks.matrix import Matrix 
from matriks.importers.csv_importer import CSVImporter
from matriks.regression.linear_regression_model import LinearRegressionModel

# ====================================================================
# FUNGSI BANTU: Metrik Evaluasi (Dipertahankan di routes.py sesuai SRP)
# ====================================================================

def calculate_r_squared(y_actual: list, y_predicted: list) -> float:
    """Menghitung R-squared (Koefisien Determinasi) secara manual."""
    ss_total = sum([(y - sum(y_actual)/len(y_actual))**2 for y in y_actual])
    ss_residual = sum([(y_actual[i] - y_predicted[i])**2 for i in range(len(y_actual))])
    
    if ss_total == 0:
        return 0.0
    return 1 - (ss_residual / ss_total)

def calculate_rmse(y_actual: list, y_predicted: list) -> float:
    """Menghitung Root Mean Squared Error (RMSE) secara manual."""
    n = len(y_actual)
    squared_errors = sum([(y_actual[i] - y_predicted[i])**2 for i in range(n)])
    return math.sqrt(squared_errors / n)

# ====================================================================
# RUTE FLASK UTAMA
# ====================================================================

bp = Blueprint("pages", __name__, url_prefix='/')

# Nama Kolom yang sudah divalidasi
FEATURE_COLUMN = "Berat_Kendaraan_kg" 
TARGET_COLUMN = "Konsumsi_Ltr_100km"
CSV_FILENAME = 'konsumsi_bahan_bakar_kendaraan.csv'

@bp.route("/about")
def about(): 
    return render_template("pages/about.html", title="Tentang Proyek")

@bp.route("/")
def home():
    """Halaman Beranda. Hanya me-render tampilan awal sebelum analisis."""
    # KOREKSI: Tambahkan FEATURE_COLUMN dan TARGET_COLUMN ke konteks template home()
    return render_template(
        "pages/analysis.html", 
        title="Beranda",
        header_title=None,
        CSV_FILENAME=CSV_FILENAME,
        feature_name=FEATURE_COLUMN, # FIX: Tambahkan variabel ini
        target_name=TARGET_COLUMN,   # FIX: Tambahkan variabel ini
        analysis_success=False
    )

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
        X_data = [[row[0]] for row in raw_data_list]
        y_data_flat = [row[1] for row in raw_data_list]
        target_matrix = Matrix([[y] for y in y_data_flat])
        
        feature_matrix = Matrix(X_data)
        
        # 3. Latih Model Regresi
        model = LinearRegressionModel()
        model.fit(feature_matrix, target_matrix)
        weights = model.get_weights() 
        
        # 4. Prediksi dan Metrik
        X_vis = [row[0] for row in X_data] 
        y_pred_vis = [model.predict(x) for x in X_vis]

        r_squared = calculate_r_squared(y_data_flat, y_pred_vis)
        rmse = calculate_rmse(y_data_flat, y_pred_vis)
        
        # 5. Interpretasi Hasil
        if weights:
            b0 = weights['intercept']
            b1 = weights['slope']
            
            interpretation = (
                f"Model Linear Regression yang dihasilkan adalah: Y = {b0:.4f} + {b1:.4f} * X. "
                f"Koefisien Determinasi (R²) sebesar {r_squared:.4f} menunjukkan {r_squared*100:.2f}% variasi dalam Konsumsi BBM dapat dijelaskan oleh Berat Kendaraan. "
                f"RMSE sebesar {rmse:.4f} adalah rata-rata deviasi prediksi dari nilai aktual."
            )
        else:
            interpretation = "Model gagal menghitung bobot."
            
        # 6. Siapkan data untuk Chart.js
        chart_data = {
            'X_data': X_vis, 
            'y_data_actual': y_data_flat,
            'y_data_predicted': y_pred_vis
        }
        
        # 7. Kirim data ke template
        return render_template(
            "pages/analysis.html",
            title="Hasil Analisis",
            header_title="Dashboard Analisis Matriks & ML",
            weights=weights,
            r_squared=r_squared,
            rmse=rmse,
            interpretation=interpretation,
            chart_data=chart_data,
            analysis_success=True,
            CSV_FILENAME=CSV_FILENAME,
            feature_name=FEATURE_COLUMN, # Variabel sudah tersedia di sini
            target_name=TARGET_COLUMN    # Variabel sudah tersedia di sini
        )

    except Exception as e:
        # Pastikan error handling juga memiliki variabel ini
        return render_template(
            "pages/analysis.html", 
            title="Error", 
            header_title="Peringatan Error Analisis", 
            error_message=f"Kesalahan Analisis: {e.__class__.__name__}: {e}", 
            analysis_success=False, 
            CSV_FILENAME=CSV_FILENAME,
            feature_name=FEATURE_COLUMN, 
            target_name=TARGET_COLUMN
        )