import os


DEBUG = True

BASE_DIR = os.path.dirname(path)

# Настройки для PostgreSQL
DATABASE = {
    'PostgreSQL': {
        'HOST': '192.168.0.178',
        'PORT': '5432',
        'DB_NAME': 'mydatabase',
        'DB_LOGIN': 'admin',
        'DB_PASSWORD': '124578zz',
    }
}

DEFAULT_DATABASE = 'PostgreSQL'
