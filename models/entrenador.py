import sqlite3
from .usuario import usuario

class entrenador(usuario):
    def __init__(self, id, email, password, nombre):
        super().__init__(id, email, password, 'entrenador', nombre)

    @staticmethod
    def get_by_id(cursor, user_id):
        query = "SELECT id, email, password, nombre FROM usuarios WHERE id = ? AND tipo_usuario = 'entrenador'"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

        if row:
            id, email, password, nombre = row
            return entrenador(id, email, password, nombre)
        else:
            return None
    
    def get_assigned_rutinas(self):
        conn = sqlite3.connect('database/fitpal.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rutinas WHERE usuario_id = ?', (self.id,))
        rutinas = cursor.fetchall()    

        conn.close()
        return rutinas
    
    def assign_rutina(self, alumno_id, nombre_ejercicio, descripcion):
        conn = sqlite3.connect('database/fitpal.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO rutinas (nombre_ejercicio, descripcion, usuario_id) VALUES (?, ?, ?)',
                       (nombre_ejercicio, descripcion, alumno_id))
        conn.commit()

        conn.close()
    
    def add_rutina(self, nombre_ejercicio, descripcion):
        conn = sqlite3.connect('database/fitpal.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO rutinas (nombre_ejercicio, descripcion, usuario_id) VALUES (?, ?, ?)',
                       (nombre_ejercicio, descripcion, self.id))
        conn.commit()

        conn.close()
    def get_rutinas(self):
        conn = sqlite3.connect('database/fitpal.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rutinas WHERE usuario_id = ?', (self.id,))
        rutinas = cursor.fetchall()

        conn.close()
        return rutinas
