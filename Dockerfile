# Dockerfile

# [1] BASE IMAGE: Menggunakan Python 3.10 FULL IMAGE (Sudah benar)
FROM python:3.10 

# [2] WORKDIR: Menetapkan direktori kerja di dalam container
WORKDIR /app

# [3] DEPENDENSI: Menyalin dan menginstal dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# [4] COPY CODE: Menyalin seluruh kode aplikasi Anda (Termasuk wsgi.py yang baru)
COPY . /app

# [5] EXPOSE: Mendeklarasikan port yang akan digunakan aplikasi
EXPOSE 5000

# [6] CMD: Menjalankan aplikasi dengan Gunicorn
# PERBAIKAN KRUSIAL: Target Gunicorn diubah dari 'flask-app:create_app' menjadi 'flask-app.wsgi:application'
# Target sekarang menunjuk ke objek aplikasi WSGI yang sudah di-instantiate di wsgi.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flask-app.wsgi:application"]