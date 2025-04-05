from models import db

class Vehiculo(db.Model):
    __tablename__ = "vehiculos"

    id = db.Column(db.Integer, primary_key=True)
    dominio = db.Column(db.String(20), unique=True, nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    gestionado = db.Column(db.Boolean, default=False)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id", ondelete="CASCADE"),  # 💥 Agregado para PostgreSQL
        nullable=False
    )

    servicios_relacion = db.relationship(
        "Servicio",
        back_populates="vehiculo",
        cascade="all, delete",
        passive_deletes=True  # 💥 Para que funcione bien la cascada con SQLAlchemy
    )

    def __repr__(self):
        return f"<Vehiculo {self.marca} {self.modelo}>"