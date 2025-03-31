from flask import Blueprint, request, jsonify
from models.cliente import Cliente  # ✅ Importación correcta
from models import db ,Cliente, Vehiculo, Servicio
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import make_response 

clientes_bp = Blueprint("clientes", __name__)

# Obtener todos los clientes



@clientes_bp.route("/", methods=["GET"])
@jwt_required()
def get_clientes():
    print("TOKEN OK")
    user_id = get_jwt_identity()
    print("🧠 Usuario autenticado:", user_id)  # Esto ahora debería mostrar el dict con nombre, email, id

    clientes = Cliente.query.all()
    return jsonify([
        {
            "id": c.id,
            "nombre": c.nombre,
            "apellido": c.apellido,
            "email": c.email,
            "cuit": c.cuit,
            "telefono": c.telefono
        } for c in clientes
    ])


@clientes_bp.route("/vehiculo/<dominio>", methods=["GET"])

def get_cliente_por_dominio(dominio):
    vehiculo = Vehiculo.query.filter_by(dominio=dominio).first()
    
    if not vehiculo or not vehiculo.cliente_id:
        return jsonify({"error": "Cliente no encontrado"}), 404

    cliente = Cliente.query.get(vehiculo.cliente_id)
    
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    return jsonify({
        "id": cliente.id,
        "nombre": cliente.nombre,
        "apellido": cliente.apellido
    })
# Obtener un cliente por ID
@clientes_bp.route("/<int:id>", methods=["GET"])
def get_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    return jsonify({
        "id": cliente.id,
        "nombre": cliente.nombre,
        "apellido": cliente.apellido,
        "email": cliente.email,
        "telefono": cliente.telefono
    })

# Crear un nuevo cliente
@clientes_bp.route("/", methods=["POST"])  # <-- Solo POST

def create_cliente():
    try:
        data = request.json

        # Verificar campos requeridos
        if not all(key in data for key in ("nombre", "apellido", "cuit", "telefono", "email")):
            return jsonify({"error": "Faltan datos requeridos"}), 400

        # Crear nuevo cliente
        nuevo_cliente = Cliente(
            nombre=data["nombre"],
            apellido=data["apellido"],
            cuit=data["cuit"],
            telefono=data["telefono"],
            email=data["email"]
        )

        db.session.add(nuevo_cliente)
        db.session.commit()

        return jsonify({"message": "Cliente creado correctamente"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear cliente: {str(e)}"}), 500

        




# Actualizar un cliente
@clientes_bp.route("/<int:id>", methods=["PUT"])

def update_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    
    data = request.json
    cliente.nombre = data.get("nombre", cliente.nombre)
    cliente.apellido = data.get("apellido", cliente.apellido)
    cliente.email = data.get("email", cliente.email)
    cliente.telefono = data.get("telefono", cliente.telefono)
    cliente.cuit = data.get("cuit", cliente.cuit)

    db.session.commit()
    return jsonify({"message": "Cliente actualizado correctamente"})

# Eliminar un cliente
@clientes_bp.route("/<int:id>", methods=["DELETE"])

def delete_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    db.session.delete(cliente)  # Esto elimina al cliente y todo lo relacionado
    db.session.commit()

    return jsonify({"message": "Cliente y sus datos eliminados correctamente"})


 # asegurate que esté importado si no lo está

@clientes_bp.route("/clientes", methods=["OPTIONS"])

def handle_clientes_options():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response