from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

_DB_HOST = config('DB_HOST')
_DB_NAME = config('DB_NAME')
_DB_USER = config('DB_USER')
_DB_PASSWORD = config('DB_PASSWORD')
_DB_PORT = config('DB_PORT', default=5432, cast=int)
_DB_DRIVER = "postgresql+psycopg2"
SQLALCHEMY_DATABASE_URI = f'{_DB_DRIVER}://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}'
