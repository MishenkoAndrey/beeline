from beeline import settings
from beeline.app import create_app

config = dict()
config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
config['FLASK_ADMIN_SWATCH'] = 'cerulean'
config['SECRET_KEY'] = 'very_secret_key'


app = create_app(**config)
