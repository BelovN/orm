import os


DEBUG = True

BASE_DIR = os.path.dirname(path)

# Настройки для PostgreSQL
DATABASE = {
    'sqlite3': {
        'DB_NAME': 'mydatabase',
    }
}

DEFAULT_DATABASE = 'sqlite3'
