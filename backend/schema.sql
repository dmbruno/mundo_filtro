-- Crear tabla de clientes
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    cuit TEXT NOT NULL,
    telefono TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de vehículos
CREATE TABLE vehiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dominio TEXT UNIQUE NOT NULL,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    anio INTEGER NOT NULL,
    cliente_id INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Crear tabla de servicios
CREATE TABLE servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehiculo_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    fecha_servicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cambio_aceite TEXT,
    filtro_aceite BOOLEAN DEFAULT 0,
    filtro_aire BOOLEAN DEFAULT 0,
    filtro_combustible BOOLEAN DEFAULT 0,
    filtro_habitaculo BOOLEAN DEFAULT 0,
    otros_servicios TEXT,
    notas TEXT,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);