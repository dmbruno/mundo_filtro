import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db
from models.cliente import Cliente
from models.vehiculo import Vehiculo
from models.servicio import Servicio
from models.usuarios import Usuario

with app.app_context():
    db.create_all()
    print("✅ Tablas creadas exitosamente en PostgreSQL.")
    print("📦 DATABASE_URL EN USO:", app.config['SQLALCHEMY_DATABASE_URI'])