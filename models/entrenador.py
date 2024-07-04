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

    @staticmethod
    def get_rutina_by_id(cursor, rutina_id):
        query = "SELECT id, nombre_ejercicio, descripcion FROM rutinas WHERE id = ?"
        cursor.execute(query, (rutina_id,))
        row = cursor.fetchone()

        if row:
            return {
                'id': row[0],
                'nombre_ejercicio': row[1],
                'descripcion': row[2]
            }
        return None

    def get_assigned_rutinas(self):
        conn = sqlite3.connect('database/fitpal.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id, nombre_ejercicio, descripcion FROM rutinas WHERE usuario_id = ?', (self.id,))
        rutinas = cursor.fetchall()    

        conn.close()
        return [{'id': row[0], 'nombre_ejercicio': row[1], 'descripcion': row[2]} for row in rutinas]

    @staticmethod
    def assign_rutina(entrenador_id, alumno_id, nombre_ejercicio, descripcion):
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

        cursor.execute('SELECT id, nombre_ejercicio, descripcion FROM rutinas WHERE usuario_id = ?', (self.id,))
        rutinas = cursor.fetchall()

        conn.close()
        return [{'id': row[0], 'nombre_ejercicio': row[1], 'descripcion': row[2]} for row in rutinas]
    @staticmethod
    def update_rutina(cursor, rutina_id, nombre_ejercicio, descripcion):
        cursor.execute('UPDATE rutinas SET nombre_ejercicio = ?, descripcion = ? WHERE id = ?', 
                       (nombre_ejercicio, descripcion, rutina_id))
    @staticmethod
    def assign_rutina_to_alumno(entrenador_id, alumno_id, nombre_ejercicio, descripcion):
        conn = sqlite3.connect('database/fitpal.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO rutinas (nombre_ejercicio, descripcion, usuario_id) VALUES (?, ?, ?)',
                       (nombre_ejercicio, descripcion, alumno_id))
        conn.commit()

        conn.close()