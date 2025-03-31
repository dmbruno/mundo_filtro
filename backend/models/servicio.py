from models import db

class Servicio(db.Model):
    __tablename__ = 'servicios'  # Asegura que SQLAlchemy busque en la tabla correcta

    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    fecha_servicio = db.Column(db.DateTime, default=db.func.current_timestamp())
    cambio_aceite = db.Column(db.String(100))
    filtro_aceite = db.Column(db.Boolean, default=False)
    filtro_aire = db.Column(db.Boolean, default=False)
    filtro_combustible = db.Column(db.Boolean, default=False)
    filtro_habitaculo = db.Column(db.Boolean, default=False)
    otros_servicios = db.Column(db.Text)
    notas = db.Column(db.Text)
    tipo_servicio = db.Column(db.String(100), nullable=True)
    kms = db.Column(db.Integer, nullable=True)
     # Relación con Vehiculo y Cliente
    # 🔥 Usar el mismo nombre en `back_populates`
    vehiculo = db.relationship("Vehiculo", back_populates="servicios_relacion")
    cliente = db.relationship("Cliente", backref="servicios")

    def __repr__(self):
        return f"<Servicio {self.id} - Vehiculo {self.vehiculo_id}>"