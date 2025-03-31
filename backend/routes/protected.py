from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

protected_bp = Blueprint("protected", __name__)

@protected_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user = get_jwt_identity()
    print("🧠 Usuario desde el token:", user)
    return jsonify({
        "msg": "Acceso autorizado 👌",
        "usuario": user
    })