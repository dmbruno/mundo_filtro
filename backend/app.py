from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from flask_jwt_extended import JWTManager
from config import Config
# Importar la base de datos correctamente
from models import db
from sqlalchemy import event  # Importar event para manejar conexiones

import sqlite3
from sqlalchemy.engine import Engine


@event.listens_for(Engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()
        
        
        
# Inicializar la app
app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

print("🔐 JWT_SECRET_KEY:", app.config['JWT_SECRET_KEY'])
# Inicializar la base de datos con la app
db.init_app(app)
migrate = Migrate(app, db)


# Para permitir solicitudes desde http://localhost:3000 específicamente
CORS(app, origins=[
    "https://mundo-filtro-frontend.vercel.app",
    "http://localhost:3000"
], supports_credentials=True)

# Crear el contexto de la aplicación para evitar errores
with app.app_context():
    # Activar claves foráneas en cada conexión
   

    # Importar modelos para que Flask los detecte
    from models.cliente import Cliente
    from models.vehiculo import Vehiculo
    from models.servicio import Servicio
    from models.usuarios import Usuario
    

# Configurar la respuesta para permitir solicitudes CORS de tu frontend


# Importar rutas
from routes.clientes import clientes_bp
from routes.vehiculos import vehiculos_bp
from routes.servicios import servicios_bp
from routes.acciones import acciones_bp
from routes.usuarios import usuarios_bp
from routes.auth import auth_bp


from routes.protected import protected_bp
app.register_blueprint(protected_bp, url_prefix="/auth")

# Registrar las rutas
app.register_blueprint(clientes_bp, url_prefix="/clientes")
app.register_blueprint(vehiculos_bp, url_prefix="/vehiculos")
app.register_blueprint(servicios_bp, url_prefix="/servicios")
app.register_blueprint(acciones_bp, url_prefix="/acciones")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

@app.route("/")
def home():
    return "¡Bienvenido a la API del lubricentro!"

if __name__ == "__main__":
    app.run(debug=True)