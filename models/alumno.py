import sqlite3
from .usuario import usuario

class alumno(usuario):
    def __init__(self, id, email, password, nombre):
        super().__init__(id, email, password, 'alumno', nombre)
    
    def get_assigned_rutinas(self):
        conn = sqlite3.connect('database/fitpal.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rutinas WHERE usuario_id = ?', (self.id,))
        rutinas = cursor.fetchall()

        conn.close()
        return rutinas
    
    def get_entrenador(self):
        conn = sqlite3.connect('database/fitpal.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM usuarios WHERE id IN (SELECT entrenador_id FROM asignaciones WHERE alumno_id = ?)', (self.id,))
        entrenador = cursor.fetchone()

        conn.close()
        return entrenador
@staticmethod
def get_by_id(cursor, id):
        query = "SELECT * FROM alumnos WHERE id = %s"
        cursor.execute(query, (id,))
        alumno_data = cursor.fetchone()
        if alumno_data:
            return alumno(alumno_data)  # Suponiendo que tienes una clase Alumno que crea un objeto alumno
        else:
            return None