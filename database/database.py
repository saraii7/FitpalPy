import sqlite3
import os

def create_connection():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),'fitpal.db')) 
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL,
            nombre TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rutinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_ejercicio TEXT NOT NULL,
            descripcion TEXT,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    cursor.execute('''
        INSERT INTO usuarios (email, password, tipo_usuario, nombre)
        VALUES ('admin@example.com', 'admin123', 'admin', 'Admin User')
    ''')

    cursor.execute('''
        INSERT INTO usuarios (email, password, tipo_usuario, nombre)
        VALUES ('trainer@example.com', 'trainer123', 'entrenador', 'John Trainer')
    ''')

    cursor.execute('''
        INSERT INTO usuarios (email, password, tipo_usuario, nombre)
        VALUES ('student@example.com', 'student123', 'alumno', 'Jane Student')
    ''')
    cursor.execute('''
        INSERT INTO rutinas (nombre_ejercicio, descripcion, usuario_id)
        VALUES ('Flexiones', 'Realizar 3 series de 15 repeticiones', 2)  -- Asignada a entrenador con usuario_id 2
    ''')

    cursor.execute('''
        INSERT INTO rutinas (nombre_ejercicio, descripcion, usuario_id)
        VALUES ('Sentadillas', 'Realizar 4 series de 12 repeticiones', 2)  -- Asignada a entrenador con usuario_id 2
    ''')

    cursor.execute('''
        INSERT INTO rutinas (nombre_ejercicio, descripcion, usuario_id)
        VALUES ('Abdominales', 'Realizar 3 series de 20 repeticiones', 3)  -- Asignada a alumno con usuario_id 3
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS asignaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrenador_id INTEGER NOT NULL,
        alumno_id INTEGER NOT NULL,
        rutina_id INTEGER NOT NULL,
        FOREIGN KEY (entrenador_id) REFERENCES usuarios (id),
        FOREIGN KEY (alumno_id) REFERENCES usuarios (id),
        FOREIGN KEY (rutina_id) REFERENCES rutinas (id)
    )
    ''')
    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_tables()