from flask import Blueprint, request, jsonify
from models import db
from models.usuarios import Usuario
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity



auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "El usuario ya existe"}), 400

    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email']
    )
    nuevo_usuario.set_password(data['password'])

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"msg": "Usuario creado correctamente"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # 🔍 Validar datos
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"msg": "Faltan credenciales"}), 400

    # 🔎 Buscar usuario en la base de datos
    usuario = Usuario.query.filter_by(email=data['email']).first()

    # 🔐 Verificar contraseña
    if usuario and usuario.check_password(data['password']):
        access_token = create_access_token(identity=str(usuario.id))
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Credenciales incorrectas"}), 401




@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    usuario = Usuario.query.get(user_id)

    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "is_admin": usuario.is_admin
    })