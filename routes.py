from flask import Blueprint, jsonify, request, render_template, send_file
from auth_utils import token_requerido
from models import Administrador, Granjero, Veterinario, AplicacionVacuna
from models import Cerdo
from models import Vacuna
from models import db
from datetime import datetime, date
import pdfkit
import io
from sqlalchemy import extract


# from flask import render_template, make_response


routes_bp = Blueprint("routes", __name__)


# Solo el administrador puede ver todos los usuarios
@routes_bp.route("/usuarios", methods=["GET"])
@token_requerido(roles_permitidos=["administrador"])
def listar_usuarios():
    admins = Administrador.query.all()
    granjeros = Granjero.query.all()
    veterinarios = Veterinario.query.all()

    return jsonify(
        {
            "administradores": [a.nombre for a in admins],
            "granjeros": [
                {
                    "id": g.id_granjero,
                    "nombre": g.nombre,
                    "apellido": g.apellido,
                    "direccion": g.direccion,
                    "telefono": g.telefono,
                }
                for g in granjeros
            ],
            "veterinarios": [
                {
                    "id": v.id_veterinario,
                    "nombre": v.nombre,
                    "apellido": v.apellido,
                    "direccion": v.direccion,
                    "telefono": v.telefono,
                }
                for v in veterinarios
            ],
        }
    )


# ========================= CERDOS ==============================

# ruta para listar cerdo por ID solo accesible por administrador y granjero

# @routes_bp.route('/cerdos/<int:id>', methods=['GET'])
# @token_requerido(roles_permitidos=['administrador', 'granjero', 'veterinario'])
# def obtener_cerdo_por_id(id):
#     cerdo = Cerdo.query.get(id)
#     if not cerdo:
#         return jsonify({'error': 'Cerdo no encontrado'}), 404

#     return jsonify({
#         'id': cerdo.id_cerdo,
#         'raza': cerdo.raza,
#         'descripcion': cerdo.descripcion,
#         'fecha_ingreso': cerdo.fecha_ingreso.isoformat() if cerdo.fecha_ingreso else None,
#         'fecha_salida': cerdo.fecha_salida.isoformat() if cerdo.fecha_salida else None,
#         'disponible': cerdo.disponible,
#         'edad': cerdo.edad,
#         'peso': cerdo.peso,
#         'id_granjero': cerdo.id_granjero,
#         'id_admin': cerdo.id_admin,
#         'fecha_creacion': cerdo.fecha_creacion.isoformat() if cerdo.fecha_creacion else None,
#         'fecha_modificacion': cerdo.fecha_modificacion.isoformat() if cerdo.fecha_modificacion else None,
#         'creado_por': cerdo.creado_por,
#         'modificado_por': cerdo.modificado_por,
#         'edad_meses': cerdo.edad_meses

#     })


@routes_bp.route("/cerdos/<int:id>", methods=["GET"])
@token_requerido(roles_permitidos=["administrador", "granjero", "veterinario"])
def obtener_cerdo_por_id(id):
    cerdo = Cerdo.query.get(id)
    if not cerdo:
        return jsonify({"error": "Cerdo no encontrado"}), 404

    return jsonify(
        {
            "id": cerdo.id_cerdo,
            "numero_arete": cerdo.numero_arete,  # 🔹 Campo nuevo agregado
            "raza": cerdo.raza,
            "descripcion": cerdo.descripcion,
            "fecha_ingreso": (
                cerdo.fecha_ingreso.isoformat() if cerdo.fecha_ingreso else None
            ),
            "fecha_salida": (
                cerdo.fecha_salida.isoformat() if cerdo.fecha_salida else None
            ),
            "disponible": cerdo.disponible,
            "edad": cerdo.edad,
            "peso": cerdo.peso,
            "id_granjero": cerdo.id_granjero,
            "id_admin": cerdo.id_admin,
            "fecha_creacion": (
                cerdo.fecha_creacion.isoformat() if cerdo.fecha_creacion else None
            ),
            "fecha_modificacion": (
                cerdo.fecha_modificacion.isoformat()
                if cerdo.fecha_modificacion
                else None
            ),
            "creado_por": cerdo.creado_por,
            "modificado_por": cerdo.modificado_por,
            "edad_meses": cerdo.edad_meses,
        }
    )


# ruta para listar cerdos solo accesible por administrador y granjero

# @routes_bp.route('/cerdos', methods=['GET'])
# @token_requerido(roles_permitidos=['administrador', 'granjero', 'veterinario'])
# def listar_cerdos():
#     cerdos = Cerdo.query.all()
#     resultado = []
#     for c in cerdos:
#         resultado.append({
#             'id': c.id_cerdo,
#             'raza': c.raza,
#             'descripcion': c.descripcion,
#             'fecha_ingreso': c.fecha_ingreso.isoformat() if c.fecha_ingreso else None,
#             'fecha_salida': c.fecha_salida.isoformat() if c.fecha_salida else None,
#             'disponible': c.disponible,
#             'edad': c.edad,
#             'peso': c.peso,
#             'id_granjero': c.id_granjero,
#             'id_admin': c.id_admin,

#             'fecha_creacion': c.fecha_creacion.isoformat() if c.fecha_creacion else None,
#             'fecha_modificacion': c.fecha_modificacion.isoformat() if c.fecha_modificacion else None,
#             'creado_por': c.creado_por,
#             'modificado_por': c.modificado_por

#         })
#     return jsonify(resultado)


@routes_bp.route("/cerdos", methods=["GET"])
@token_requerido(roles_permitidos=["administrador", "granjero", "veterinario"])
def listar_cerdos():
    cerdos = Cerdo.query.all()
    resultado = []
    for c in cerdos:
        resultado.append(
            {
                "id": c.id_cerdo,
                "numero_arete": c.numero_arete,  # 🔹 Campo nuevo agregado
                "raza": c.raza,
                "descripcion": c.descripcion,
                "fecha_ingreso": (
                    c.fecha_ingreso.isoformat() if c.fecha_ingreso else None
                ),
                "fecha_salida": c.fecha_salida.isoformat() if c.fecha_salida else None,
                "disponible": c.disponible,
                "edad": c.edad,
                "peso": c.peso,
                "id_granjero": c.id_granjero,
                "id_admin": c.id_admin,
                "fecha_creacion": (
                    c.fecha_creacion.isoformat() if c.fecha_creacion else None
                ),
                "fecha_modificacion": (
                    c.fecha_modificacion.isoformat() if c.fecha_modificacion else None
                ),
                "creado_por": c.creado_por,
                "modificado_por": c.modificado_por,
            }
        )
    return jsonify(resultado)


# ruta POST para agregar un cerdo (solo administrador y granjero)

# @routes_bp.route('/cerdos', methods=['POST'])
# @token_requerido(roles_permitidos=['administrador', 'granjero'])
# def crear_cerdo():
#     data = request.get_json()
#     creador=f"{request.rol}_{request.usuario_id}"

#     nuevo_cerdo = Cerdo(
#         raza=data.get('raza'),
#         descripcion=data.get('descripcion'),
#         fecha_ingreso=data.get('fecha_ingreso'),
#         fecha_salida=data.get('fecha_salida'),
#         disponible=data.get('disponible', True),
#         edad=data.get('edad'),
#         peso=data.get('peso'),
#         id_granjero=request.usuario_id if request.rol == 'granjero' else data.get('id_granjero'),
#         id_admin=request.usuario_id if request.rol == 'administrador' else None,
#         creado_por=creador

#     )
#     db.session.add(nuevo_cerdo)
#     db.session.commit()
#     return jsonify({'mensaje': 'Cerdo creado', 'id': nuevo_cerdo.id_cerdo}), 201


@routes_bp.route("/cerdos", methods=["POST"])
@token_requerido(roles_permitidos=["administrador", "granjero"])
def crear_cerdo():
    data = request.get_json()
    creador = f"{request.rol}_{request.usuario_id}"

    # Validación: numero_arete obligatorio
    numero_arete = data.get("numero_arete")
    if not numero_arete:
        return jsonify({"error": "El campo numero_arete es obligatorio"}), 400

    # Validación: numero_arete único
    if Cerdo.query.filter_by(numero_arete=numero_arete).first():
        return jsonify({"error": "Ya existe un cerdo con ese numero_arete"}), 409

    nuevo_cerdo = Cerdo(
        numero_arete=numero_arete,
        raza=data.get("raza"),
        descripcion=data.get("descripcion"),
        fecha_ingreso=data.get("fecha_ingreso"),
        fecha_salida=data.get("fecha_salida"),
        disponible=data.get("disponible", True),
        edad=data.get("edad"),
        peso=data.get("peso"),
        id_granjero=(
            request.usuario_id if request.rol == "granjero" else data.get("id_granjero")
        ),
        id_admin=request.usuario_id if request.rol == "administrador" else None,
        creado_por=creador,
    )

    db.session.add(nuevo_cerdo)
    db.session.commit()

    return jsonify({"mensaje": "Cerdo creado", "id": nuevo_cerdo.id_cerdo}), 201


# routes/cerdo_routes.py
# actualizar un cerdo
# @cerdo_bp.route('/cerdos/<int:id>', methods=['PUT'])
# @routes_bp.route('/cerdos/<int:id>', methods=['PUT'])
# @token_requerido(roles_permitidos=['administrador', 'granjero'])
# def actualizar_cerdo(id):
#     data = request.get_json()
#     cerdo = Cerdo.query.get(id)

#     if not cerdo:
#         return jsonify({'error': 'Cerdo no encontrado'}), 404


#     cerdo.raza = data.get('raza', cerdo.raza)
#     cerdo.descripcion = data.get('descripcion', cerdo.descripcion)
#     cerdo.fecha_ingreso = data.get('fecha_ingreso', cerdo.fecha_ingreso)
#     cerdo.fecha_salida = data.get('fecha_salida', cerdo.fecha_salida)
#     cerdo.disponible = data.get('disponible', cerdo.disponible)
#     cerdo.edad = data.get('edad', cerdo.edad)
#     cerdo.peso = data.get('peso', cerdo.peso)
#     cerdo.modificado_por = f"{request.rol}_{request.usuario_id}"


#     db.session.commit()
#     return jsonify({'mensaje': 'Cerdo actualizado correctamente'})


@routes_bp.route("/cerdos/<int:id>", methods=["PUT"])
@token_requerido(roles_permitidos=["administrador", "granjero"])
def actualizar_cerdo(id):
    data = request.get_json()
    cerdo = Cerdo.query.get(id)

    if not cerdo:
        return jsonify({"error": "Cerdo no encontrado"}), 404

    # Si se desea actualizar el numero_arete, verificar que sea único
    nuevo_numero_arete = data.get("numero_arete")
    if nuevo_numero_arete and nuevo_numero_arete != cerdo.numero_arete:
        if Cerdo.query.filter_by(numero_arete=nuevo_numero_arete).first():
            return jsonify({"error": "Ya existe otro cerdo con ese numero_arete"}), 409
        cerdo.numero_arete = nuevo_numero_arete

    cerdo.raza = data.get("raza", cerdo.raza)
    cerdo.descripcion = data.get("descripcion", cerdo.descripcion)
    cerdo.fecha_ingreso = data.get("fecha_ingreso", cerdo.fecha_ingreso)
    cerdo.fecha_salida = data.get("fecha_salida", cerdo.fecha_salida)
    cerdo.disponible = data.get("disponible", cerdo.disponible)
    cerdo.edad = data.get("edad", cerdo.edad)
    cerdo.peso = data.get("peso", cerdo.peso)
    cerdo.modificado_por = f"{request.rol}_{request.usuario_id}"

    db.session.commit()

    return jsonify({"mensaje": "Cerdo actualizado correctamente"})


# eliminar un cerdo
# @cerdo_bp.route('/cerdos/<int:id>', methods=['DELETE'])
@routes_bp.route("/cerdos/<int:id>", methods=["DELETE"])
@token_requerido(roles_permitidos=["administrador", "granjero"])
def eliminar_cerdo(id):
    cerdo = Cerdo.query.get(id)

    if not cerdo:
        return jsonify({"error": "Cerdo no encontrado"}), 404

    # Solo el granjero que lo creó o un admin puede eliminarlo
    # if request.rol == 'granjero' and cerdo.id_granjero != request.usuario_id:
    #     return jsonify({'error': 'No tienes permiso para eliminar este cerdo'}), 403

    db.session.delete(cerdo)
    db.session.commit()
    return jsonify({"mensaje": "Cerdo eliminado correctamente"})


# consultar historial vacunacion


@routes_bp.route("/cerdos/<int:id>/historial", methods=["GET"])
@token_requerido(roles_permitidos=["administrador", "veterinario", "granjero"])
def historial_vacunacion(id):
    aplicaciones = AplicacionVacuna.query.filter_by(id_cerdo=id).all()
    resultado = []
    for app in aplicaciones:
        resultado.append(
            {
                "id_aplicacion": app.id_aplicacion,
                "nombre_vacuna": app.vacuna.nombre if app.vacuna else None,
                "fecha_aplicacion": app.fecha_aplicacion.isoformat(),
                "descripcion": app.descripcion,
            }
        )
    return jsonify(resultado)


# Buscar cerdo por numero del arete


@routes_bp.route("/cerdos/arete/<string:numero_arete>", methods=["GET"])
@token_requerido(roles_permitidos=["administrador", "granjero", "veterinario"])
def obtener_cerdo_por_arete(numero_arete):
    cerdo = Cerdo.query.filter_by(numero_arete=numero_arete).first()

    if not cerdo:
        return jsonify({"error": "Cerdo no encontrado"}), 404

    return jsonify(
        {
            "id": cerdo.id_cerdo,
            "numero_arete": cerdo.numero_arete,
            "raza": cerdo.raza,
            "descripcion": cerdo.descripcion,
            "fecha_ingreso": (
                cerdo.fecha_ingreso.isoformat() if cerdo.fecha_ingreso else None
            ),
            "fecha_salida": (
                cerdo.fecha_salida.isoformat() if cerdo.fecha_salida else None
            ),
            "disponible": cerdo.disponible,
            "edad": cerdo.edad,
            "peso": cerdo.peso,
            "id_granjero": cerdo.id_granjero,
            "id_admin": cerdo.id_admin,
            "fecha_creacion": (
                cerdo.fecha_creacion.isoformat() if cerdo.fecha_creacion else None
            ),
            "fecha_modificacion": (
                cerdo.fecha_modificacion.isoformat()
                if cerdo.fecha_modificacion
                else None
            ),
            "creado_por": cerdo.creado_por,
            "modificado_por": cerdo.modificado_por,
            "edad_meses": cerdo.edad_meses,
        }
    )


# ========================= VACUNAS ==============================

# Obtener vacuna por ID


@routes_bp.route("/vacunas/<int:id>", methods=["GET"])
@token_requerido(roles_permitidos=["administrador", "veterinario", "granjero"])
def obtener_vacuna_por_id(id):
    vacuna = Vacuna.query.get(id)
    if not vacuna:
        return jsonify({"error": "Vacuna no encontrada"}), 404

    return jsonify(
        {
            "id": vacuna.id_vacuna,
            "nombre": vacuna.nombre,
            "descripcion": vacuna.descripcion,
            "fecha_vencimiento": vacuna.fecha_vencimiento.isoformat(),
            "id_admin": vacuna.id_admin,
            "id_granjero": vacuna.id_granjero,
            "id_veterinario": vacuna.id_veterinario,
            "fecha_creacion": (
                vacuna.fecha_creacion.isoformat() if vacuna.fecha_creacion else None
            ),
            "fecha_modificacion": (
                vacuna.fecha_modificacion.isoformat()
                if vacuna.fecha_modificacion
                else None
            ),
            "creado_por": vacuna.creado_por,
            "modificado_por": vacuna.modificado_por,
        }
    )


# Obtener todas las vacunas
@routes_bp.route("/vacunas", methods=["GET"])
@token_requerido(roles_permitidos=["administrador", "granjero", "veterinario"])
def listar_vacunas():
    vacunas = Vacuna.query.all()
    resultado = []
    for v in vacunas:
        resultado.append(
            {
                "id_vacuna": v.id_vacuna,
                "nombre": v.nombre,
                "descripcion": v.descripcion,
                "fecha_vencimiento": (
                    v.fecha_vencimiento.isoformat()
                    if isinstance(v.fecha_vencimiento, (date, datetime))
                    else v.fecha_vencimiento
                ),
                "id_admin": v.id_admin,
                "id_granjero": v.id_granjero,
                "id_veterinario": v.id_veterinario,
                # Campos de auditoría:
                "fecha_creacion": (
                    v.fecha_creacion.isoformat() if v.fecha_creacion else None
                ),
                "fecha_modificacion": (
                    v.fecha_modificacion.isoformat() if v.fecha_modificacion else None
                ),
                "creado_por": v.creado_por,
                "modificado_por": v.modificado_por,
            }
        )
    return jsonify(resultado)


# Crear una nueva vacuna
@routes_bp.route("/vacunas", methods=["POST"])
@token_requerido(roles_permitidos=["administrador", "veterinario", "granjero"])
def crear_vacuna():
    data = request.get_json()
    creador = f"{request.rol}_{request.usuario_id}"

    nueva_vacuna = Vacuna(
        nombre=data["nombre"],
        descripcion=data.get("descripcion"),
        fecha_vencimiento=data["fecha_vencimiento"],
        id_admin=request.usuario_id if request.rol == "administrador" else None,
        id_veterinario=(
            request.usuario_id
            if request.rol == "veterinario"
            else data.get("id_veterinario")
        ),
        # AUDITORIA
        fecha_creacion=datetime.utcnow(),
        creado_por=creador,
    )
    db.session.add(nueva_vacuna)
    db.session.commit()
    return jsonify({"mensaje": "Vacuna registrada", "id": nueva_vacuna.id_vacuna}), 201


# Actualizar una vacuna
@routes_bp.route("/vacunas/<int:id>", methods=["PUT"])
@token_requerido(roles_permitidos=["administrador", "veterinario", "granjero"])
def actualizar_vacuna(id):
    vacuna = Vacuna.query.get(id)

    if not vacuna:
        return jsonify({"error": "Vacuna no encontrada"}), 404

    data = request.get_json()
    vacuna.nombre = data.get("nombre", vacuna.nombre)
    vacuna.descripcion = data.get("descripcion", vacuna.descripcion)
    vacuna.fecha_vencimiento = data.get("fecha_vencimiento", vacuna.fecha_vencimiento)

    # auditoria
    vacuna.fecha_modificacion = datetime.utcnow()
    vacuna.modificado_por = f"{request.rol}_{request.usuario_id}"

    db.session.commit()
    return jsonify({"mensaje": "Vacuna actualizada"})


# Eliminar una vacuna
@routes_bp.route("/vacunas/<int:id>", methods=["DELETE"])
@token_requerido(roles_permitidos=["administrador", "granjero", "veterinario"])
def eliminar_vacuna(id):
    vacuna = Vacuna.query.get(id)
    if not vacuna:
        return jsonify({"error": "Vacuna no encontrada"}), 404
    db.session.delete(vacuna)
    db.session.commit()
    return jsonify({"mensaje": "Vacuna eliminada correctamente"})


# ========================= APLICACION VACUNAS ==============================

# CREAR aplicación de vacuna
# @routes_bp.route('/aplicaciones', methods=['POST'])
# @token_requerido(roles_permitidos=['veterinario'])
# def crear_aplicacion():
#     data = request.get_json()
#     creador = f"{request.rol}_{request.usuario_id}"

#     nueva_aplicacion = AplicacionVacuna(
#         id_vacuna=data['id_vacuna'],
#         id_cerdo=data['id_cerdo'],
#         fecha_aplicacion=datetime.strptime(data['fecha_aplicacion'], '%Y-%m-%d'),
#         descripcion=data.get('descripcion'),
#         id_veterinario=request.usuario_id,

#         fecha_creacion=datetime.utcnow(),
#         creado_por=creador
#     )


#     db.session.add(nueva_aplicacion)
#     db.session.commit()
#     return jsonify({'mensaje': 'Aplicación de vacuna registrada'}), 201
@routes_bp.route("/aplicaciones", methods=["POST"])
@token_requerido(roles_permitidos=["veterinario"])
def crear_aplicacion():
    data = request.get_json()
    creador = f"{request.rol}_{request.usuario_id}"

    id_cerdo = data.get("id_cerdo")
    id_vacuna = data.get("id_vacuna")
    fecha_aplicacion_str = data.get("fecha_aplicacion")

    # 1. Validar que el cerdo exista
    cerdo = Cerdo.query.get(id_cerdo)
    if not cerdo:
        return jsonify({"error": "El cerdo especificado no existe"}), 400

    # 2. Validar formato de fecha
    try:
        fecha_aplicacion = datetime.strptime(fecha_aplicacion_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    # 3. Verificar duplicado
    duplicado = AplicacionVacuna.query.filter_by(
        id_cerdo=id_cerdo, id_vacuna=id_vacuna, fecha_aplicacion=fecha_aplicacion
    ).first()

    if duplicado:
        return (
            jsonify(
                {
                    "error": "Ya existe una aplicación de esta vacuna para este cerdo en esa fecha"
                }
            ),
            409,
        )

    # 4. Crear nueva aplicación
    nueva_aplicacion = AplicacionVacuna(
        id_cerdo=id_cerdo,
        id_vacuna=id_vacuna,
        fecha_aplicacion=fecha_aplicacion,
        descripcion=data.get("descripcion"),
        id_veterinario=request.usuario_id,
        creado_por=creador,
        fecha_creacion=datetime.utcnow(),
    )

    db.session.add(nueva_aplicacion)
    db.session.commit()

    return jsonify({"mensaje": "Aplicación registrada correctamente"}), 201


# LISTAR aplicaciones de vacunas (admin y veterinario)
@routes_bp.route("/aplicaciones", methods=["GET"])
@token_requerido(roles_permitidos=["administrador", "veterinario", "granjero"])
def listar_aplicaciones():
    aplicaciones = AplicacionVacuna.query.all()
    resultado = []
    for app in aplicaciones:
        resultado.append(
            {
                "id_aplicacion": app.id_aplicacion,
                "id_vacuna": app.id_vacuna,
                "id_cerdo": app.id_cerdo,
                "fecha_aplicacion": app.fecha_aplicacion.isoformat(),
                "id_veterinario": app.id_veterinario,
                "descripcion": app.descripcion,
                "fecha_creacion": (
                    app.fecha_creacion.isoformat() if app.fecha_creacion else None
                ),
                "fecha_modificacion": (
                    app.fecha_modificacion.isoformat()
                    if app.fecha_modificacion
                    else None
                ),
                "creado_por": app.creado_por,
                "modificado_por": app.modificado_por,
            }
        )
    return jsonify(resultado), 200


# ACTUALIZAR una aplicación de vacuna
# @routes_bp.route('/aplicaciones/<int:id>', methods=['PUT'])
# @token_requerido(roles_permitidos=['veterinario'])
# def actualizar_aplicacion(id):
#     aplicacion = AplicacionVacuna.query.get(id)
#     if not aplicacion:
#         return jsonify({'error': 'Aplicación no encontrada'}), 404
#     if aplicacion.id_veterinario != request.usuario_id:
#         return jsonify({'error': 'No tienes permiso para modificar esta aplicación'}), 403

#     data = request.get_json()
#     aplicacion.id_vacuna = data.get('id_vacuna', aplicacion.id_vacuna)
#     aplicacion.id_cerdo = data.get('id_cerdo', aplicacion.id_cerdo)
#     if 'fecha_aplicacion' in data:
#         aplicacion.fecha_aplicacion = datetime.strptime(data['fecha_aplicacion'], '%Y-%m-%d')
#         aplicacion.descripcion = data.get('descripcion', aplicacion.descripcion)

#     # Agregar auditoría
#     aplicacion.fecha_modificacion = datetime.utcnow()
#     aplicacion.modificado_por = f"{request.rol}_{request.usuario_id}"

#     db.session.commit()
#     return jsonify({'mensaje': 'Aplicación actualizada correctamente'})


@routes_bp.route("/aplicaciones/<int:id>", methods=["PUT"])
@token_requerido(roles_permitidos=["veterinario"])
def actualizar_aplicacion(id):
    aplicacion = AplicacionVacuna.query.get(id)
    if not aplicacion:
        return jsonify({"error": "Aplicación no encontrada"}), 404

    if aplicacion.id_veterinario != request.usuario_id:
        return (
            jsonify({"error": "No tienes permiso para modificar esta aplicación"}),
            403,
        )

    data = request.get_json()

    # Obtener nuevos valores o mantener actuales
    nuevo_id_vacuna = data.get("id_vacuna", aplicacion.id_vacuna)
    nuevo_id_cerdo = data.get("id_cerdo", aplicacion.id_cerdo)
    nueva_fecha_aplicacion = aplicacion.fecha_aplicacion  # valor por defecto

    # Validar si se quiere modificar la fecha
    if "fecha_aplicacion" in data:
        try:
            nueva_fecha_aplicacion = datetime.strptime(
                data["fecha_aplicacion"], "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    # Validar que el cerdo existe (solo si se quiere cambiar)
    if nuevo_id_cerdo != aplicacion.id_cerdo:
        cerdo = Cerdo.query.get(nuevo_id_cerdo)
        if not cerdo:
            return jsonify({"error": "El cerdo especificado no existe"}), 400

    # Validar que no haya duplicado (otra aplicación distinta con mismos valores)
    duplicado = AplicacionVacuna.query.filter(
        AplicacionVacuna.id != id,
        AplicacionVacuna.id_cerdo == nuevo_id_cerdo,
        AplicacionVacuna.id_vacuna == nuevo_id_vacuna,
        AplicacionVacuna.fecha_aplicacion == nueva_fecha_aplicacion,
    ).first()

    if duplicado:
        return (
            jsonify(
                {"error": "Ya existe otra aplicación con esta vacuna, cerdo y fecha"}
            ),
            409,
        )

    # Aplicar cambios
    aplicacion.id_vacuna = nuevo_id_vacuna
    aplicacion.id_cerdo = nuevo_id_cerdo
    aplicacion.fecha_aplicacion = nueva_fecha_aplicacion
    aplicacion.descripcion = data.get("descripcion", aplicacion.descripcion)
    aplicacion.fecha_modificacion = datetime.utcnow()
    aplicacion.modificado_por = f"{request.rol}_{request.usuario_id}"

    db.session.commit()
    return jsonify({"mensaje": "Aplicación actualizada correctamente"}), 200


# ELIMINAR una aplicación de vacuna
@routes_bp.route("/aplicaciones/<int:id>", methods=["DELETE"])
@token_requerido(roles_permitidos=["veterinario"])
def eliminar_aplicacion(id):
    aplicacion = AplicacionVacuna.query.get(id)
    if not aplicacion:
        return jsonify({"error": "Aplicación no encontrada"}), 404
    if aplicacion.id_veterinario != request.usuario_id:
        return (
            jsonify({"error": "No tienes permiso para eliminar esta aplicación"}),
            403,
        )

    db.session.delete(aplicacion)
    db.session.commit()
    return jsonify({"mensaje": "Aplicación eliminada correctamente"})


#  aplicaciones de vacuna por ID
@routes_bp.route("/aplicaciones/<int:id>", methods=["GET"])
@token_requerido(roles_permitidos=["administrador", "veterinario", "granjero"])
def obtener_aplicacion_por_id(id):
    aplicacion = AplicacionVacuna.query.get(id)
    if not aplicacion:
        return jsonify({"error": "Aplicación no encontrada"}), 404

    resultado = {
        "id": aplicacion.id_aplicacion,
        "id_cerdo": aplicacion.id_cerdo,
        "id_vacuna": aplicacion.id_vacuna,
        "id_veterinario": aplicacion.id_veterinario,
        "fecha_aplicacion": (
            aplicacion.fecha_aplicacion.isoformat()
            if aplicacion.fecha_aplicacion
            else None
        ),
        "descripcion": aplicacion.descripcion,
        "fecha_creacion": (
            aplicacion.fecha_creacion.isoformat() if aplicacion.fecha_creacion else None
        ),
        "fecha_modificacion": (
            aplicacion.fecha_modificacion.isoformat()
            if aplicacion.fecha_modificacion
            else None
        ),
        "creado_por": aplicacion.creado_por,
        "modificado_por": aplicacion.modificado_por,
    }

    return jsonify(resultado)


# ============ALERTA DE VACUNACION============================


@routes_bp.route("/alertas/proximas-vacunas", methods=["GET"])
@token_requerido(roles_permitidos=["granjero"])
def alertas_vacunas():
    from datetime import timedelta

    hoy = datetime.utcnow().date()
    proxima_fecha = hoy + timedelta(days=7)

    aplicaciones = AplicacionVacuna.query.filter(
        AplicacionVacuna.fecha_aplicacion >= hoy,
        AplicacionVacuna.fecha_aplicacion <= proxima_fecha,
    ).all()

    resultado = []
    for app in aplicaciones:
        resultado.append(
            {
                "cerdo_id": app.id_cerdo,
                "vacuna": app.vacuna.nombre,
                "fecha_aplicacion": app.fecha_aplicacion.isoformat(),
            }
        )
    return jsonify(resultado)


@routes_bp.route("/reporte-mensual", methods=["GET"])
# @jwt_required()
def generar_reporte_mensual():

    hoy = datetime.today()
    mes = int(request.args.get("mes", hoy.month))
    anio = int(request.args.get("anio", hoy.year))

    # Consulta a la base de datos
    cerdos = Cerdo.query.filter(
        extract("month", Cerdo.fecha_ingreso) == mes,
        extract("year", Cerdo.fecha_ingreso) == anio,
    ).all()

    # Si no hay cerdos registrados ese mes
    if not cerdos:
        return jsonify({"mensaje": "No hay cerdos ingresados en este mes"}), 200

    lista_cerdos = [
        {
            "id": cerdo.id_cerdo,
            "numero_arete": cerdo.numero_arete,
            "descripcion": cerdo.descripcion,
            "peso": cerdo.peso,
            "raza": cerdo.raza,
            "fecha_ingreso": cerdo.fecha_ingreso.strftime("%d-%m-%Y"),
        }
        for cerdo in cerdos
    ]

    import base64
    import os

    # Ruta absoluta del logo (ajusta si tu logo tiene otro nombre o ubicación)
    ruta_logo = os.path.abspath("static/logo.png")

    # Leer y codificar el logo en base64
    with open(ruta_logo, "rb") as img_file:
        logo_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    html = render_template(
        "reporte_mensual.html",
        cerdos=lista_cerdos,
        mes=mes,
        anio=anio,
        fecha_actual=hoy,
        logo_b64=logo_b64,
    )

    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Users\usuario\Desktop\html\wkhtmltox\bin\wkhtmltopdf.exe"
    )
    pdf = pdfkit.from_string(html, False, configuration=config)

    return send_file(
        io.BytesIO(pdf),
        download_name=f"reporte_mensual_{mes}_{anio}.pdf",
        as_attachment=True,
    )
