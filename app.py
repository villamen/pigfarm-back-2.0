# from flask import Flask
# from flask_bcrypt import Bcrypt
# from flask_cors import CORS
# from models import db
# from config import Config
# from auth import auth_bp
# from routes import routes_bp
# from perfil import perfil_bp

# # Crear y configurar la aplicación
# app = Flask(__name__)
# app.config.from_object(Config)

# # Habilitar CORS para todas las rutas
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Puedes usar "*" para todos los orígenes
# #CORS(app, resources={r"/*": {"origins": ["http://localhost", "http://localhost:80"]}})


# # Inicializar extensiones
# db.init_app(app)
# bcrypt = Bcrypt(app)

# # Registrar blueprints
# app.register_blueprint(auth_bp)
# app.register_blueprint(routes_bp)
# app.register_blueprint(perfil_bp)

# # Ruta raíz de prueba
# @app.route('/')
# def index():
#     return {'mensaje': 'API PigFarm funcionando'}

# # Crear las tablas si no existen
# with app.app_context():
#     db.create_all()

# # Ejecutar la app
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db
from config import Config
from auth import auth_bp
from routes import routes_bp
from perfil import perfil_bp
import os

# Crear y configurar la aplicación
app = Flask(__name__)
app.config.from_object(Config)

# Habilitar CORS para todas las rutas
# Cambia "*" por la URL de tu frontend cuando la tengas desplegada
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializar extensiones
db.init_app(app)
bcrypt = Bcrypt(app)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)
app.register_blueprint(perfil_bp)

# Ruta raíz de prueba
@app.route('/')
def index():
    return {'mensaje': 'API PigFarm funcionando'}

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# Ejecutar la app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render asigna el puerto automáticamente
    app.run(host="0.0.0.0", port=port, debug=True)































# from flask import Flask
# from flask_bcrypt import Bcrypt
# from models import db
# from config import Config
# from auth import auth_bp
# from routes import routes_bp
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Esto habilita CORS para todas las rutas




# # Crear app Flask
# app = Flask(__name__)
# app.config.from_object(Config)

# # Inicializar extensiones
# db.init_app(app)
# bcrypt = Bcrypt(app)

# # Registrar blueprints
# app.register_blueprint(auth_bp)
# app.register_blueprint(routes_bp)
# #app.register_blueprint(cerdo_bp)

# # Ruta raíz de prueba
# @app.route('/')
# def index():
#     return {'mensaje': 'API PigFarm funcionando'}

# # Crear las tablas si no existen (solo en desarrollo)
# with app.app_context():
#     db.create_all()

# # Iniciar servidor
# if __name__ == '__main__':
#     app.run(debug=True)
