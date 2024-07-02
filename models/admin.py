import sqlite3

from .usuario import usuario

class admin(usuario):
    def __init__(self, id, email, password, nombre):
        super().__init__(id, email, password, 'admin', nombre)

    @staticmethod
    def get_all_rutinas(cursor):
        cursor.execute('SELECT id, nombre_ejercicio, descripcion FROM rutinas')
        rutinas = []
        for row in cursor.fetchall():
            rutina = {
                'id':row [0],
                'nombre_ejercicio':row[1],
                'descripcion': row[2]
            }
            rutinas.append(rutina)
        return rutinas
    @staticmethod
    def delete_rutina(cursor,rutina_id):

        cursor.execute('DELETE FROM rutinas WHERE id = ?', (rutina_id,))
        

    @staticmethod
    def update_rutina(cursor,rutina_id, nombre_ejercicio, descripcion):
        cursor.execute('UPDATE rutinas SET nombre_ejercicio = ?, descripcion = ? WHERE id = ?', (nombre_ejercicio, descripcion, rutina_id))
      

    @staticmethod
    def get_rutina_by_id(cursor,rutina_id):
       query = "SELECT id, nombre_ejercicio, descripcion FROM rutinas WHERE id = ?"
       cursor.execute(query, (rutina_id,))
       row = cursor.fetchone()

       if row:
            rutina = {
                'id': row[0],
                'nombre_ejercicio': row[1],
                'descripcion': row[2]
            }
            return rutina
       else:
            return None
