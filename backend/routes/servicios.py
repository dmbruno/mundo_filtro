from flask import Blueprint, request, jsonify
from models.servicio import Servicio
from models.vehiculo import Vehiculo
from models.cliente import Cliente
from models import db
from flask_cors import CORS
from flask import make_response
from flask_jwt_extended import jwt_required 

servicios_bp = Blueprint("servicios", __name__)

# Obtener todos los servicios
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func

@servicios_bp.route("/", methods=["GET"])

def get_servicios():
    # Subquery: obtener el ID del último servicio por cada vehículo
    subquery = (
        db.session.query(
            Servicio.vehiculo_id, 
            func.max(Servicio.fecha_servicio).label("max_fecha")  # Obtiene la fecha más reciente
        )
        .group_by(Servicio.vehiculo_id)  # Agrupa por vehículo
        .subquery()
    )

    # Query principal: obtener los servicios que coincidan con la fecha más reciente por vehículo
    servicios = (
        db.session.query(Servicio)
        .join(subquery, (Servicio.vehiculo_id == subquery.c.vehiculo_id) & (Servicio.fecha_servicio == subquery.c.max_fecha))
        .options(joinedload(Servicio.vehiculo), joinedload(Servicio.cliente))  # Carga relaciones
        .all()
    )

    # Convertir los resultados en JSON
    servicios_response = [{
        "id": s.id,
        "fecha_servicio": s.fecha_servicio,
        "cambio_aceite": s.cambio_aceite,
        "filtro_aceite": s.filtro_aceite,
        "filtro_aire": s.filtro_aire,
        "filtro_combustible": s.filtro_combustible,
        "filtro_habitaculo": s.filtro_habitaculo,
        "otros_servicios": s.otros_servicios,
        "notas": s.notas,
        "vehiculo": {
            "id": s.vehiculo.id,
            "dominio": s.vehiculo.dominio,
            "marca": s.vehiculo.marca,
            "modelo": s.vehiculo.modelo
        },
        "cliente": {
            "id": s.cliente.id if s.cliente else None,
            "nombre": s.cliente.nombre if s.cliente else "Sin Cliente",
            "apellido": s.cliente.apellido if s.cliente else ""
        }
    } for s in servicios]

    return jsonify(servicios_response)


@servicios_bp.route("/vehiculo/<int:vehiculo_id>", methods=["GET"])

def get_servicios_por_vehiculo(vehiculo_id):
    servicios = (
        db.session.query(
            Servicio.id,
            Servicio.fecha_servicio,
            Servicio.cambio_aceite,
            Servicio.filtro_aceite,
            Servicio.kms, 
            Servicio.filtro_aire,
            Servicio.filtro_combustible,
            Servicio.filtro_habitaculo,
            Servicio.otros_servicios,
            Servicio.tipo_servicio,
            Servicio.notas,
            Vehiculo.id.label("vehiculo_id"),
            Vehiculo.dominio,
            Vehiculo.marca,
            Vehiculo.modelo,
            Cliente.id.label("cliente_id"),  # 📌 Aseguramos que traiga el ID del cliente
            Cliente.nombre,
            Cliente.apellido
        )
        .join(Vehiculo, Servicio.vehiculo_id == Vehiculo.id)
        .join(Cliente, Servicio.cliente_id == Cliente.id)
        .filter(Servicio.vehiculo_id == vehiculo_id)
        .all()
    )

    # Convertir los resultados en JSON
    servicios_response = []
    for servicio in servicios:
        servicios_response.append({
            "id": servicio.id,
            "fecha_servicio": servicio.fecha_servicio,
            "cambio_aceite": servicio.cambio_aceite,
            "filtro_aceite": servicio.filtro_aceite,
            "filtro_aire": servicio.filtro_aire,
            "filtro_combustible": servicio.filtro_combustible,
            "filtro_habitaculo": servicio.filtro_habitaculo,
            "kms": servicio.kms, 
            "tipo_servicio": servicio.tipo_servicio,
            "otros_servicios": servicio.otros_servicios,
            "notas": servicio.notas,
            "vehiculo": {
                "id": servicio.vehiculo_id,
                "dominio": servicio.dominio,
                "marca": servicio.marca,
                "modelo": servicio.modelo
            },
            "cliente": {  # 📌 Aseguramos que el cliente SIEMPRE esté presente
                "id": servicio.cliente_id,
                "nombre": servicio.nombre,
                "apellido": servicio.apellido
            }
        })

    return jsonify(servicios_response)

@servicios_bp.route("/", methods=["POST"])

def create_servicio():
    data = request.json
    print("📥 Datos recibidos en POST:", data)

    # Si cliente_id no viene en la petición, devolver error
    cliente_id = data.get("cliente_id")
    if cliente_id is None:
        return jsonify({"error": "cliente_id es obligatorio"}), 400

    vehiculo = Vehiculo.query.get(data.get("vehiculo_id"))
    cliente = Cliente.query.get(cliente_id)

    if not vehiculo:
        return jsonify({"error": "Vehículo no encontrado"}), 404
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    try:
        nuevo_servicio = Servicio(
            vehiculo_id=data["vehiculo_id"],
            cliente_id=cliente_id,  # ← Aquí usamos el cliente_id validado
            kms=data.get("kms", 0),
            tipo_servicio=data.get("tipo_servicio", 0),
            cambio_aceite=data.get("cambio_aceite"),
            filtro_aceite=data.get("filtro_aceite", 0),
            filtro_aire=data.get("filtro_aire", 0),
            filtro_combustible=data.get("filtro_combustible", 0),
            filtro_habitaculo=data.get("filtro_habitaculo", 0),
            otros_servicios=data.get("otros_servicios"),
            notas=data.get("notas")
        )
        db.session.add(nuevo_servicio)
        db.session.commit()
        return jsonify({"message": "Servicio registrado correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        print("❌ Error al guardar el servicio:", str(e))
        return jsonify({"error": str(e)}), 500

# Eliminar un servicio
@servicios_bp.route("/<int:id>", methods=["DELETE"])

def delete_servicio(id):
    servicio = Servicio.query.get(id)
    if not servicio:
        return jsonify({"error": "Servicio no encontrado"}), 404

    try:
        db.session.delete(servicio)
        db.session.commit()
        return jsonify({"message": "Servicio eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    
    
@servicios_bp.route("/<int:id>", methods=["PUT"])

def actualizar_servicio(id):
    servicio = Servicio.query.get(id)
    if not servicio:
        return jsonify({"error": "Servicio no encontrado"}), 404

    data = request.json

    # ✅ Agregar kms y tipo_servicio
    servicio.kms = data.get("kms", servicio.kms)  # Asegurar que kms se actualiza
    servicio.tipo_servicio = data.get("tipo_servicio", servicio.tipo_servicio)  # Asegurar que tipo_servicio se actualiza

    servicio.cambio_aceite = data.get("cambio_aceite", servicio.cambio_aceite)
    servicio.filtro_aceite = data.get("filtro_aceite", servicio.filtro_aceite)
    servicio.filtro_aire = data.get("filtro_aire", servicio.filtro_aire)
    servicio.filtro_combustible = data.get("filtro_combustible", servicio.filtro_combustible)
    servicio.filtro_habitaculo = data.get("filtro_habitaculo", servicio.filtro_habitaculo)
    servicio.otros_servicios = data.get("otros_servicios", servicio.otros_servicios)
    servicio.notas = data.get("notas", servicio.notas)

    try:
        db.session.commit()
        return jsonify({
            "message": "Servicio actualizado con éxito",
            "servicio": {
                "id": servicio.id,
                "kms": servicio.kms,  # ✅ Ahora se devuelve kms
                "tipo_servicio": servicio.tipo_servicio,  # ✅ Ahora se devuelve tipo_servicio
                "cambio_aceite": servicio.cambio_aceite,
                "filtro_aceite": servicio.filtro_aceite,
                "filtro_aire": servicio.filtro_aire,
                "filtro_combustible": servicio.filtro_combustible,
                "filtro_habitaculo": servicio.filtro_habitaculo,
                "otros_servicios": servicio.otros_servicios,
                "notas": servicio.notas
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar servicio: {str(e)}"}), 500
    
    
@servicios_bp.route("/servicios", methods=["OPTIONS"])

def handle_options():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response