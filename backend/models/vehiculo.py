from models import db

class Vehiculo(db.Model):
    __tablename__ = "vehiculos"  # ✅ Asegura que coincida con la BD

    id = db.Column(db.Integer, primary_key=True)
    dominio = db.Column(db.String(20), unique=True, nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)  # ✅ Asegurar clave foránea
    servicios_relacion = db.relationship("Servicio", back_populates="vehiculo", cascade="all, delete")
    
    def __repr__(self):
        return f"<Vehiculo {self.marca} {self.modelo}>"