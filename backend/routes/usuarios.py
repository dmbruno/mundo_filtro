from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.usuarios import Usuario
from models import db

usuarios_bp = Blueprint("usuarios", __name__)

# 🔐 Verificar si el usuario actual es admin
def is_admin():
    user_id = get_jwt_identity()
    user = Usuario.query.get(user_id)
    return user and user.is_admin

# 📄 Obtener todos los usuarios
@usuarios_bp.route("/", methods=["GET"])
@jwt_required()
def obtener_usuarios():
    if not is_admin():
        return jsonify({"msg": "Acceso denegado"}), 403

    usuarios = Usuario.query.all()
    return jsonify([
        {
            "id": u.id,
            "nombre": u.nombre,
            "email": u.email,
            "is_admin": u.is_admin
        } for u in usuarios
    ])

# ➕ Crear un nuevo usuario
@usuarios_bp.route("/", methods=["POST"])
@jwt_required()
def crear_usuario():
    if not is_admin():
        return jsonify({"msg": "Acceso denegado"}), 403

    data = request.get_json()
    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "El email ya está en uso"}), 400

    nuevo = Usuario(
        nombre=data["nombre"],
        email=data["email"],
        is_admin=data.get("is_admin", False)
    )
    nuevo.set_password(data["password"])
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"msg": "Usuario creado correctamente"}), 201

# 🛠 Actualizar un usuario
@usuarios_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_usuario(id):
    if not is_admin():
        return jsonify({"msg": "Acceso denegado"}), 403

    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    data = request.get_json()
    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.email = data.get("email", usuario.email)
    usuario.is_admin = data.get("is_admin", usuario.is_admin)

    if "password" in data:
        usuario.set_password(data["password"])

    db.session.commit()
    return jsonify({"msg": "Usuario actualizado correctamente"}), 200

# 🗑 Eliminar un usuario
@usuarios_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_usuario(id):
    if not is_admin():
        return jsonify({"msg": "Acceso denegado"}), 403

    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"msg": "Usuario eliminado"}), 200


