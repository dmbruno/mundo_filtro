from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
# Importar los modelos aquí para que sean reconocidos por SQLAlchemy
from models.usuarios import Usuario
from models.cliente import Cliente
from models.vehiculo import Vehiculo
from models.servicio import Servicio