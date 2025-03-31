from models import db

class Cliente(db.Model):  # <-- Nombre correcto
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cuit = db.Column(db.String, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relación con vehículos (¡corregir nombre de la clase!)
    vehiculos = db.relationship("Vehiculo", backref="cliente", cascade="all, delete")  # <-- "Vehiculo", no "Vehículo"

    def __repr__(self):  # <-- Método bien escrito
        return f"<Cliente {self.nombre} {self.apellido}>"