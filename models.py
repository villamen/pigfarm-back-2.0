from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Administrador(db.Model):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    granjeros = db.relationship('Granjero', backref='administrador', lazy=True)
    veterinarios = db.relationship('Veterinario', backref='administrador', lazy=True)
    vacunas = db.relationship('Vacuna', backref='admin', lazy=True)
    cerdos = db.relationship('Cerdo', backref='admin', lazy=True)

class Granjero(db.Model):
    __tablename__ = 'granjero'
    id_granjero = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    id_admin = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=True)
    vacunas = db.relationship('Vacuna', backref='granjero', lazy=True)
    cerdos = db.relationship('Cerdo', backref='granjero', lazy=True)

   

class Veterinario(db.Model):
    __tablename__ = 'veterinario'
    id_veterinario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    id_admin = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=True)
    vacunas = db.relationship('Vacuna', backref='veterinario', lazy=True)
    aplicaciones = db.relationship('AplicacionVacuna', backref='veterinario', lazy=True)

# class Cerdo(db.Model):
#     __tablename__ = 'cerdo'
#     id_cerdo = db.Column(db.Integer, primary_key=True)
#     raza = db.Column(db.String(100), nullable=False)
#     descripcion = db.Column(db.String(255))
#     fecha_ingreso = db.Column(db.Date)
#     fecha_salida = db.Column(db.Date)
#     disponible = db.Column(db.Boolean, default=True)
#     edad = db.Column(db.Integer, nullable=False)
#     peso = db.Column(db.Float, nullable=False)

#     id_granjero = db.Column(db.Integer, db.ForeignKey('granjero.id_granjero'), nullable=True)
#     id_admin = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=True)

#     aplicaciones = db.relationship('AplicacionVacuna', backref='cerdo', lazy=True)

#      # Auditoría
#     fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
#     fecha_modificacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
#     creado_por = db.Column(db.String(50))
#     modificado_por = db.Column(db.String(50))
    
#     #funcion para averiguar la edad de un animal
#     @property
#     def edad_meses(self):
#       if not self.fecha_ingreso:
#         return None
#       hoy = datetime.utcnow().date()
#       return (hoy.year - self.fecha_ingreso.year) * 12 + hoy.month - self.fecha_ingreso.month

#from datetime import datetime
#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

class Cerdo(db.Model):
    __tablename__ = 'cerdo'

    id_cerdo = db.Column(db.Integer, primary_key=True)
    
    # 🔹 Nuevo campo agregado
    numero_arete = db.Column(db.String(10), unique=True, nullable=False)

    raza = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    fecha_ingreso = db.Column(db.Date)
    fecha_salida = db.Column(db.Date)
    disponible = db.Column(db.Boolean, default=True)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)

    id_granjero = db.Column(db.Integer, db.ForeignKey('granjero.id_granjero'), nullable=True)
    id_admin = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=True)

    # aplicaciones = db.relationship('AplicacionVacuna', backref='cerdo', lazy=True)
    aplicaciones = db.relationship(
        'AplicacionVacuna',
        backref='cerdo',
        lazy=True,
        passive_deletes=True  # 🔹 Para que SQLAlchemy no intente poner id_cerdo = NULL
    )

    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    creado_por = db.Column(db.String(50))
    modificado_por = db.Column(db.String(50))

    # Función para averiguar la edad en meses
    @property
    def edad_meses(self):
        if not self.fecha_ingreso:
            return None
        hoy = datetime.utcnow().date()
        return (hoy.year - self.fecha_ingreso.year) * 12 + hoy.month - self.fecha_ingreso.month


class Vacuna(db.Model):
    __tablename__ = 'vacuna'
    id_vacuna = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    fecha_vencimiento = db.Column(db.Date, nullable=False)

    id_admin = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=True)
    id_granjero = db.Column(db.Integer, db.ForeignKey('granjero.id_granjero'), nullable=True)
    id_veterinario = db.Column(db.Integer, db.ForeignKey('veterinario.id_veterinario'), nullable=True)

    # aplicaciones = db.relationship('AplicacionVacuna', backref='vacuna', lazy=True)
    # aplicaciones = db.relationship(
    #     'AplicacionVacuna',
    #     backref='vacuna',
    #     lazy=True,
    #     passive_deletes=True  # 🔹 Para que SQLAlchemy no intente poner id_cerdo = NULL
    # )
    aplicaciones = db.relationship('AplicacionVacuna', backref='vacuna', lazy=True)

    #auditoria

    fecha_creacion = db.Column(db.DateTime)
    fecha_modificacion = db.Column(db.DateTime)
    creado_por = db.Column(db.String(50))
    modificado_por = db.Column(db.String(50))

class AplicacionVacuna(db.Model):
    __tablename__ = 'aplicacion_vacuna'
    id_aplicacion = db.Column(db.Integer, primary_key=True)
    # id_cerdo = db.Column(db.Integer, db.ForeignKey('cerdo.id_cerdo'), nullable=False)
    id_cerdo = db.Column(db.Integer,db.ForeignKey('cerdo.id_cerdo', ondelete='CASCADE'),nullable=False)
    id_veterinario = db.Column(db.Integer, db.ForeignKey('veterinario.id_veterinario', ondelete='SET NULL'), nullable=False)
    id_vacuna = db.Column(db.Integer, db.ForeignKey('vacuna.id_vacuna', ondelete='SET NULL'), nullable=False)
    fecha_aplicacion = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(255))

#auditoria
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    creado_por = db.Column(db.String(50))
    modificado_por = db.Column(db.String(50))
