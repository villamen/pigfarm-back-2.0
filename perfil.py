from flask import Blueprint, request, jsonify
from models import db, Administrador, Granjero, Veterinario
from auth_utils import token_requerido
from flask_bcrypt import Bcrypt

perfil_bp = Blueprint('perfil', __name__)
bcrypt = Bcrypt()

# Mapeo de roles a modelos
MODELOS = {
    'administrador': Administrador,
    'granjero': Granjero,
    'veterinario': Veterinario
}

# Obtener perfil del usuario logueado
@perfil_bp.route('/perfil', methods=['GET'])
@token_requerido()
def obtener_perfil():
    rol = request.rol
    usuario_id = request.usuario_id
    modelo = MODELOS.get(rol)

    if not modelo:
        return jsonify({'error': 'Rol inválido'}), 400

    if rol == 'administrador':
        usuario = modelo.query.get(usuario_id)
    else:
        usuario = modelo.query.filter(getattr(modelo, f'id_{rol}') == usuario_id).first()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    datos = {
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'direccion': usuario.direccion,
        'telefono': getattr(usuario, 'telefono', None),
        'rol': rol
    }
    return jsonify(datos), 200


# Actualizar perfil del usuario logueado
@perfil_bp.route('/perfil', methods=['PUT'])
@token_requerido()
def actualizar_perfil():
    rol = request.rol
    usuario_id = request.usuario_id
    modelo = MODELOS.get(rol)

    if not modelo:
        return jsonify({'error': 'Rol inválido'}), 400

    if rol == 'administrador':
        usuario = modelo.query.get(usuario_id)
    else:
        usuario = modelo.query.filter(getattr(modelo, f'id_{rol}') == usuario_id).first()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()
    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.apellido = data.get('apellido', usuario.apellido)
    usuario.direccion = data.get('direccion', usuario.direccion)

    if rol != 'administrador':
        usuario.telefono = data.get('telefono', usuario.telefono)

    if data.get('password'):
        usuario.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    db.session.commit()
    return jsonify({'mensaje': 'Perfil actualizado con éxito'}), 200
