from flask import Blueprint, request, jsonify
from models.vehiculo import Vehiculo
from models.cliente import Cliente  # Importar Cliente
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import make_response 

from models.servicio import Servicio

vehiculos_bp = Blueprint("vehiculos", __name__)

# Obtener todos los vehículos con el nombre y apellido del cliente
from models import Vehiculo, Cliente

@vehiculos_bp.route("/", methods=["GET"])  # <-- Método GET correcto
@jwt_required()
def get_vehiculos():
    user_id = get_jwt_identity()
    print("📦 Usuario autenticado:", user_id)
    vehiculos = db.session.query(
        Vehiculo.id, 
        Vehiculo.dominio, 
        Vehiculo.marca, 
        Vehiculo.modelo,
        Vehiculo.anio, 
        Cliente.nombre, 
        Cliente.apellido
    ).join(Cliente, Vehiculo.cliente_id == Cliente.id).all()

    return jsonify([{
        "id": v.id,
        "dominio": v.dominio,
        "marca": v.marca,
        "modelo": v.modelo,
        "anio": v.anio,
        "cliente": f"{v.nombre} {v.apellido}"  # <-- Formato correcto
    } for v in vehiculos])

# Obtener un vehículo por ID
# Obtener todos los vehículos de un cliente específico
@vehiculos_bp.route("/cliente/<int:cliente_id>", methods=["GET"])

def get_vehiculos_por_cliente(cliente_id):
    vehiculos = Vehiculo.query.filter_by(cliente_id=cliente_id).all()

    if not vehiculos:
        return jsonify([])

    return jsonify([
        {
            "id": v.id,
            "dominio": v.dominio,
            "marca": v.marca,
            "modelo": v.modelo,
            "anio": v.anio,
            "cliente_id": v.cliente_id  # Incluimos cliente_id para referencias
        }
        for v in vehiculos
    ])

# Crear un nuevo vehículo
# Crear un nuevo vehículo
@vehiculos_bp.route("/", methods=["POST"])

def create_vehiculo():
    data = request.json
    nuevo_vehiculo = Vehiculo(
        dominio=data["dominio"],
        marca=data["marca"],
        modelo=data["modelo"],
        anio=data["anio"],  # Año añadido aquí
        cliente_id=data["cliente_id"]  # Asociamos el vehículo al cliente
    )
    db.session.add(nuevo_vehiculo)
    db.session.commit()
    return jsonify({"message": "Vehículo creado correctamente"}), 201

# Actualizar un vehículo




@vehiculos_bp.route("/<int:id>", methods=["PUT"])
def update_vehiculo(id):
    vehiculo = Vehiculo.query.get(id)
    if not vehiculo:
        return jsonify({"error": "Vehículo no encontrado"}), 404
    
    data = request.json
    nuevo_cliente_id = data.get("cliente_id")

    # ✅ Si se actualiza el cliente, también actualizamos los servicios asociados
    if nuevo_cliente_id and nuevo_cliente_id != vehiculo.cliente_id:
        vehiculo.cliente_id = nuevo_cliente_id
        db.session.query(Servicio).filter_by(vehiculo_id=id).update({"cliente_id": nuevo_cliente_id})

    # ✅ Actualizamos los otros datos del vehículo
    vehiculo.dominio = data.get("dominio", vehiculo.dominio)
    vehiculo.marca = data.get("marca", vehiculo.marca)
    vehiculo.modelo = data.get("modelo", vehiculo.modelo)
    vehiculo.anio = data.get("anio", vehiculo.anio)

    db.session.commit()
    return jsonify({"message": "Vehículo y servicios reasignados correctamente"}), 200






@vehiculos_bp.route("/<int:id>", methods=["DELETE"])

def delete_vehiculo(id):
    vehiculo = Vehiculo.query.get(id)
    if not vehiculo:
        return jsonify({"error": "Vehículo no encontrado"}), 404

    db.session.delete(vehiculo)
    db.session.commit()
    return jsonify({"message": "Vehículo eliminado correctamente"})


 # si aún no está importado

@vehiculos_bp.route("/vehiculos", methods=["OPTIONS"])

def handle_vehiculos_options():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response