from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, Administrador, Granjero, Veterinario
import jwt
import datetime
from config import Config
from auth_utils import token_requerido
####

# ####
auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# 🔐 Generar token JWT
def generar_token(usuario_id, rol):
    payload = {
        'usuario_id': usuario_id,
        'rol': rol,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')


####


# 📌 Ruta: Registro de usuarios
####
@auth_bp.route('/register', methods=['POST'])
@token_requerido(roles_permitidos=['administrador'])  # Solo admins pueden acceder
def register():
    data = request.get_json()
    rol = data.get('rol')

    if rol not in ['administrador', 'granjero', 'veterinario']:
        return jsonify({'error': 'Rol inválido'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    if rol == 'administrador':
        nuevo = Administrador(
            nombre=data['nombre'],
            apellido=data['apellido'],
            direccion=data['direccion'],
            password=hashed_password
        )
    elif rol == 'granjero':
        nuevo = Granjero(
            nombre=data['nombre'],
            apellido=data['apellido'],
            direccion=data['direccion'],
            telefono=data['telefono'],
            password=hashed_password,
            id_admin=request.usuario_id  # ID del admin extraído del token
        )
    else:  # veterinario
        nuevo = Veterinario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            direccion=data['direccion'],
            telefono=data['telefono'],
            password=hashed_password,
            id_admin=request.usuario_id
        )

    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': f'{rol.capitalize()} registrado exitosamente'}), 201

###

# 📌 Ruta: Login de usuarios

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    direccion = data.get('direccion')
    password = data.get('password')

    if not direccion or not password:
        return jsonify({'error': 'Faltan datos'}), 400

    usuario = None
    rol_detectado = None

    # Buscar el usuario por dirección en los tres modelos
    for modelo, rol in [(Administrador, 'administrador'), (Veterinario, 'veterinario'), (Granjero, 'granjero')]:
        usuario = modelo.query.filter_by(direccion=direccion).first()
        if usuario and bcrypt.check_password_hash(usuario.password, password):
            rol_detectado = rol
            break

    if not usuario or not rol_detectado:
        return jsonify({'error': 'Credenciales inválidas'}), 401

    # Obtener ID compatible
    id_usuario = usuario.id if rol_detectado == 'administrador' else getattr(usuario, f'id_{rol_detectado}')

    # Generar token JWT
    token = generar_token(id_usuario, rol_detectado)

    nombre = getattr(usuario, 'nombre', '')
    apellido = getattr(usuario, 'apellido', '')

    return jsonify({
        'token': token,
        'rol': rol_detectado,
        'nombre': nombre,
        'apellido': apellido
    }), 200


# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     direccion = data.get('direccion')
#     password = data.get('password')
#     rol = data.get('rol')

#     modelo = {'administrador': Administrador, 'granjero': Granjero, 'veterinario': Veterinario}.get(rol)
#     if not modelo:
#         return jsonify({'error': 'Rol inválido'}), 400

#     usuario = modelo.query.filter_by(direccion=direccion).first()
#     if usuario and bcrypt.check_password_hash(usuario.password, password):
#         id_usuario = usuario.id if rol == 'administrador' else getattr(usuario, f'id_{rol}')
#         token = generar_token(id_usuario, rol)

#         # Extraemos nombre y apellido si existen en el modelo
#         nombre = getattr(usuario, 'nombre', '')
#         apellido = getattr(usuario, 'apellido', '')

#         return jsonify({
#             'token': token,
#             'rol': rol,
#             'nombre': nombre,
#             'apellido': apellido
#         })

#     return jsonify({'error': 'Credenciales inválidas'}), 401

@auth_bp.route('/usuarios/<int:id>', methods=['PUT'])
@token_requerido(roles_permitidos=['administrador'])
def actualizar_usuario(id):
    data = request.get_json()
    usuario = None

    # Buscar en los 3 roles
    for modelo in [ Granjero, Veterinario]:
        usuario = modelo.query.get(id)
        if usuario:
            break

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Actualizar campos básicos
    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.apellido = data.get('apellido', usuario.apellido)
    usuario.direccion = data.get('direccion', usuario.direccion)
    usuario.telefono = data.get('telefono', usuario.telefono)

    # Actualizar contraseña si viene una nueva
    nueva_password = data.get('password')
    if nueva_password:
        usuario.password = bcrypt.generate_password_hash(nueva_password).decode('utf-8')

    db.session.commit()
    return jsonify({'mensaje': 'Usuario actualizado correctamente'}), 200



@auth_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@token_requerido(roles_permitidos=['administrador'])
def eliminar_usuario(id):
    usuario = None

    # Buscar en los modelos permitidos
    for modelo in [Granjero, Veterinario]:
        usuario = modelo.query.get(id)
        if usuario:
            break

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200



# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     direccion = data.get('direccion')
#     password = data.get('password')
#     rol = data.get('rol')

#     modelo = {'administrador': Administrador, 'granjero': Granjero, 'veterinario': Veterinario}.get(rol)
#     if not modelo:
#         return jsonify({'error': 'Rol inválido'}), 400

#     usuario = modelo.query.filter_by(direccion=direccion).first()
#     if usuario and bcrypt.check_password_hash(usuario.password, password):
#         token = generar_token(usuario.id if rol == 'administrador' else getattr(usuario, f'id_{rol}'), rol)
#         return jsonify({'token': token})
    
#     return jsonify({'error': 'Credenciales inválidas'}), 401


