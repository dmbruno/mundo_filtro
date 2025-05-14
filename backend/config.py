import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 🔄 Convertir postgres:// a postgresql:// si hace falta
database_url = os.getenv("DATABASE_URL", "")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = database_url if database_url else 'sqlite:///' + os.path.join(BASE_DIR, 'mundo_filtro.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False