from flask import request, jsonify
import jwt
from functools import wraps
from config import Config

# 🎯 Decorador que requiere autenticación y un rol específico (opcional)
def token_requerido(roles_permitidos=None):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None

            # Leer token del encabezado Authorization: Bearer <token>
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]

            if not token:
                return jsonify({'error': 'Token no proporcionado'}), 401

            try:
                data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
                usuario_id = data['usuario_id']
                rol = data['rol']

                # Verificar rol si se requiere
                if roles_permitidos and rol not in roles_permitidos:
                    return jsonify({'error': 'No autorizado para este recurso'}), 403

                # Agregar info útil al request
                request.usuario_id = usuario_id
                request.rol = rol

            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expirado'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Token inválido'}), 401

            return func(*args, **kwargs)

        return wrapper
    return decorador


