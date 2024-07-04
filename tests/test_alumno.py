import unittest
import sqlite3
from models.alumno import alumno

class TestAlumno(unittest.TestCase):
    def setUp(self):
        # Conexión a la base de datos de prueba
        self.conn = sqlite3.connect(':memory:')  # Usar una base de datos en memoria para pruebas
        self.cursor = self.conn.cursor()
        
        # Crear tablas necesarias para la prueba
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                tipo_usuario TEXT NOT NULL,
                nombre TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rutinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_ejercicio TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Insertar un alumno y rutinas de prueba
        self.cursor.execute('''
            INSERT INTO usuarios (email, password, tipo_usuario, nombre)
            VALUES ('test@example.com', 'password123', 'alumno', 'Test Alumno')
        ''')
        self.alumno_id = self.cursor.lastrowid
        self.cursor.execute('''
            INSERT INTO rutinas (nombre_ejercicio, descripcion, usuario_id)
            VALUES ('Push Ups', '10 reps', ?)
        ''', (self.alumno_id,))
        self.cursor.execute('''
            INSERT INTO rutinas (nombre_ejercicio, descripcion, usuario_id)
            VALUES ('Squats', '15 reps', ?)
        ''', (self.alumno_id,))
        self.conn.commit()
    
    def tearDown(self):
        # Cerrar la conexión a la base de datos
        self.conn.close()

    def test_get_assigned_rutinas(self):
        # Crear instancia de Alumno
        test_alumno = alumno(self.alumno_id, 'test@example.com', 'password123', 'Test Alumno')

        # Llamar a la función get_assigned_rutinas
        rutinas = test_alumno.get_assigned_rutinas()

        # Verificar que se obtienen las rutinas correctas
        self.assertEqual(len(rutinas), 2)
        self.assertEqual(rutinas[0][1], 'Push Ups')
        self.assertEqual(rutinas[1][1], 'Squats')

if __name__ == '__main__':
    unittest.main()
