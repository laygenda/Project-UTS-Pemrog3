# flask-app/__init__.py

from flask import Flask
# Impor Blueprint dari sub-paket 'pages'.
from .pages import bp as pages_bp 

def create_app():
    """
    Application Factory Flask.
    Fungsi ini adalah modul tingkat tinggi yang mengatur komponen aplikasi.
    """
    app = Flask(__name__)

    # Konfigurasi di sini (jika ada)
    # app.config.from_mapping(...)

    # Mendaftarkan Blueprint
    app.register_blueprint(pages_bp) 

    return app