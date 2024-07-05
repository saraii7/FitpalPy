import unittest
from app import app, get_db_connection
import sqlite3

class TestLogin(unittest.TestCase):

    def setUp(self):
        # Configurar el cliente de pruebas
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Crear una conexión a la base de datos de pruebas en memoria
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        # Crear tablas y agregar datos de prueba
        self.create_tables()

    def tearDown(self):
        # Cerrar la conexión a la base de datos de pruebas
        self.conn.close()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                tipo_usuario TEXT NOT NULL,
                nombre TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE rutinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_ejercicio TEXT NOT NULL,
                descripcion TEXT,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        self.cursor.execute('''
            INSERT INTO usuarios (email, password, tipo_usuario, nombre)
            VALUES ('admin@example.com', 'admin123', 'admin', 'Admin User')
        ''')
        self.cursor.execute('''
            INSERT INTO usuarios (email, password, tipo_usuario, nombre)
            VALUES ('trainer@example.com', 'trainer123', 'entrenador', 'John Trainer')
        ''')
        self.cursor.execute('''
            INSERT INTO usuarios (email, password, tipo_usuario, nombre)
            VALUES ('student@example.com', 'student123', 'alumno', 'Jane Student')
        ''')
        self.conn.commit()

    def test_login_success(self):
        # Simular una solicitud POST para iniciar sesión
        response = self.app.post('/login', data=dict(
            email='admin@example.com',
            password='admin123'
        ), follow_redirects=True)

        # Verificar que la respuesta contiene el título del dashboard de admin
        self.assertIn(b'Dashboard de Administrador', response.data)

    def test_login_failure(self):
        # Simular una solicitud POST para iniciar sesión con credenciales incorrectas
        response = self.app.post('/login', data=dict(
            email='wrong_email@example.com',
            password='wrong_password'
        ), follow_redirects=True)

        # Verificar que la respuesta contiene el mensaje de error
        self.assertIn(b'credenciales de login incorretas!', response.data)

if __name__ == '__main__':
    unittest.main()
