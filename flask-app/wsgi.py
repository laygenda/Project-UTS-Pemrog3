# flask-app/wsgi.py

import os
from .__init__ import create_app

# Gunicorn akan memanggil objek 'application' ini.
# Objek ini memanggil create_app() tanpa argumen, yang kemudian mengembalikan objek Flask.
application = create_app()