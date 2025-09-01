--creacion de base de datos
CREATE DATABASE IF NOT EXISTS pigfarm;

USE pigfarm;

CREATE TABLE administrador (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE granjero (
    id_granjero INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    password VARCHAR(255) NOT NULL,
    id_admin INT,
    FOREIGN KEY (id_admin) REFERENCES administrador(id) ON DELETE SET NULL
);

CREATE TABLE veterinario (
    id_veterinario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    password VARCHAR(255) NOT NULL,
    id_admin INT,
    FOREIGN KEY (id_admin) REFERENCES administrador(id) ON DELETE SET NULL
);

CREATE TABLE cerdo (
    id_cerdo INT PRIMARY KEY AUTO_INCREMENT,
    numero_arete VARCHAR(10) UNIQUE NOT NULL,
    raza VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    fecha_ingreso DATE,
    fecha_salida DATE,
    disponible BOOLEAN DEFAULT TRUE,
    edad INT NOT NULL,
    peso FLOAT NOT NULL,
    id_granjero INT,
    id_admin INT,
    fecha_creacion DATETIME,
    fecha_modificacion DATETIME,
    creado_por VARCHAR(50),
    modificado_por VARCHAR(50),
    FOREIGN KEY (id_granjero) REFERENCES granjero(id_granjero) ON DELETE SET NULL,
    FOREIGN KEY (id_admin) REFERENCES administrador(id) ON DELETE SET NULL
);

CREATE TABLE vacuna (
    id_vacuna INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    fecha_vencimiento DATE  NULL,
    id_admin INT,
    id_granjero INT,
    id_veterinario INT,
    fecha_creacion DATETIME,
    fecha_modificacion DATETIME,
    creado_por VARCHAR(50),
    modificado_por VARCHAR(50),
    FOREIGN KEY (id_admin) REFERENCES administrador(id) ON DELETE SET NULL,
    FOREIGN KEY (id_granjero) REFERENCES granjero(id_granjero) ON DELETE SET NULL,
    FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_veterinario) ON DELETE SET NULL
);

CREATE TABLE aplicacion_vacuna (
    id_aplicacion INT PRIMARY KEY AUTO_INCREMENT,
    id_cerdo INT NOT NULL,
    id_veterinario INT NULL,
    id_vacuna INT  NULL,
    fecha_aplicacion DATE NOT NULL,
    descripcion VARCHAR(255),
    fecha_creacion DATETIME,
    fecha_modificacion DATETIME,
    creado_por VARCHAR(50),
    modificado_por VARCHAR(50),
    FOREIGN KEY (id_cerdo) REFERENCES cerdo(id_cerdo) ON DELETE CASCADE,
    FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_veterinario) ON DELETE SET NULL,
    FOREIGN KEY (id_vacuna) REFERENCES vacuna(id_vacuna) ON DELETE SET NULL
);