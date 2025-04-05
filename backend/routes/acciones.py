from flask import Blueprint, jsonify, request
from models import db, Cliente, Vehiculo, Servicio

acciones_bp = Blueprint("acciones", __name__)

@acciones_bp.route("/exportar-datos", methods=["GET"])
def exportar_datos():
    try:
        resultados = db.session.query(
            Cliente.id.label("cliente_id"),
            Cliente.nombre,
            Cliente.apellido,
            Cliente.email,
            Cliente.cuit,
            Cliente.telefono,
            Cliente.fecha_registro,

            Vehiculo.id.label("vehiculo_id"),
            Vehiculo.dominio,
            Vehiculo.marca,
            Vehiculo.modelo,
            Vehiculo.anio,

            Servicio.id.label("servicio_id"),
            Servicio.fecha_servicio,
            Servicio.kms,
            Servicio.tipo_servicio,
            Servicio.cambio_aceite,
            Servicio.filtro_aceite,
            Servicio.filtro_aire,
            Servicio.filtro_combustible,
            Servicio.filtro_habitaculo,
            Servicio.otros_servicios,
            Servicio.notas
        ).outerjoin(Vehiculo, Vehiculo.cliente_id == Cliente.id)\
         .outerjoin(Servicio, Servicio.vehiculo_id == Vehiculo.id)\
         .all()

        datos = []
        for r in resultados:
            datos.append({
                # Cliente
                "Cliente ID": r.cliente_id,
                "Nombre": r.nombre,
                "Apellido": r.apellido,
                "Email": r.email,
                "CUIT": r.cuit,
                "Teléfono": r.telefono,
                "Fecha Registro": r.fecha_registro.strftime("%d/%m/%Y") if r.fecha_registro else "",

                # Vehículo
                "Vehículo ID": r.vehiculo_id or "",
                "Dominio": r.dominio or "",
                "Marca": r.marca or "",
                "Modelo": r.modelo or "",
                "Año": r.anio or "",

                # Servicio
                "Servicio ID": r.servicio_id or "",
                "Fecha Servicio": r.fecha_servicio.strftime("%d/%m/%Y") if r.fecha_servicio else "",
                "KMs": r.kms or "",
                "Tipo Servicio": r.tipo_servicio or "",
                "Cambio Aceite": r.cambio_aceite or "",
                "Filtro Aceite": r.filtro_aceite if r.filtro_aceite is not None else "",
                "Filtro Aire": r.filtro_aire if r.filtro_aire is not None else "",
                "Filtro Combustible": r.filtro_combustible if r.filtro_combustible is not None else "",
                "Filtro Habitáculo": r.filtro_habitaculo if r.filtro_habitaculo is not None else "",
                "Otros Servicios": r.otros_servicios or "",
                "Notas": r.notas or ""
            })

        return jsonify(datos)

    except Exception as e:
        print("❌ Error al exportar:", e)
        return jsonify({"error": str(e)}), 500
    
    
    
from flask import Blueprint, jsonify
from models import db, Cliente, Servicio
from sqlalchemy.sql import func



# 🆕 Obtener clientes con fecha del último servicio
@acciones_bp.route("/clientes-con-ultimo-servicio", methods=["GET"])
def clientes_con_ultimo_servicio():
    try:
        subconsulta = (
            db.session.query(
                Servicio.cliente_id,
                func.max(Servicio.fecha_servicio).label("ultimo_servicio")
            )
            .group_by(Servicio.cliente_id)
            .subquery()
        )

        resultados = (
            db.session.query(
                Cliente.id,
                Cliente.nombre,
                Cliente.apellido,
                Cliente.telefono,
                subconsulta.c.ultimo_servicio
            )
            .outerjoin(subconsulta, Cliente.id == subconsulta.c.cliente_id)
            .all()
        )

        clientes = []
        for r in resultados:
            clientes.append({
                "id": r.id,
                "nombre": r.nombre,
                "apellido": r.apellido,
                "telefono": r.telefono,
                "ultimo_servicio": r.ultimo_servicio.strftime("%Y-%m-%d") if r.ultimo_servicio else None
            })

        return jsonify(clientes)

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500
    
    
from sqlalchemy import func, desc


@acciones_bp.route("/vehiculos-con-ultimo-servicio", methods=["GET"])
def vehiculos_con_ultimo_servicio():
    try:
        subconsulta = db.session.query(
            Servicio.vehiculo_id,
            func.max(Servicio.fecha_servicio).label("ultimo_servicio")
        ).group_by(Servicio.vehiculo_id).subquery()

        resultados = db.session.query(
            Cliente.id.label("cliente_id"),
            Cliente.nombre,
            Cliente.apellido,
            Cliente.telefono,
            Vehiculo.id.label("vehiculo_id"),
            Vehiculo.marca,
            Vehiculo.modelo,
            Vehiculo.dominio,
            subconsulta.c.ultimo_servicio
        ).join(Vehiculo, Vehiculo.cliente_id == Cliente.id) \
         .outerjoin(subconsulta, subconsulta.c.vehiculo_id == Vehiculo.id) \
         .filter(Vehiculo.gestionado == False) \
         .order_by(Cliente.apellido, Cliente.nombre)

        datos = []
        for r in resultados:
            datos.append({
                "cliente_id": r.cliente_id,
                "nombre": r.nombre,
                "apellido": r.apellido,
                "telefono": r.telefono,
                "vehiculo_id": r.vehiculo_id,
                "marca": r.marca,
                "modelo": r.modelo,
                "dominio": r.dominio,
                "ultimo_servicio": r.ultimo_servicio.strftime("%Y-%m-%d") if r.ultimo_servicio else None
            })

        return jsonify(datos)

    except Exception as e:
        print("❌ Error al traer vehículos con último servicio:", e)
        return jsonify({"error": str(e)}), 500
    
    
    
@acciones_bp.route('/marcar-gestionado/<int:vehiculo_id>', methods=['PUT'])
def marcar_gestionado(vehiculo_id):
    vehiculo = Vehiculo.query.get(vehiculo_id)

    if not vehiculo:
        return jsonify({"error": "Vehículo no encontrado"}), 404

    vehiculo.gestionado = True

    try:
        db.session.commit()
        return jsonify({"message": "Vehículo marcado como gestionado"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al marcar gestionado: {str(e)}"}), 500
    