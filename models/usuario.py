import sqlite3
from database.database import create_connection
def create_connection():
    conn = sqlite3.connect('database/fitpal.db')
    return conn

class usuario:
    def __init__(self, id, email, password, tipo_usuario, nombre=None):
        self.id = id
        self.email = email
        self.password = password
        self.tipo_usuario = tipo_usuario
        self.nombre = nombre

    @classmethod
    def login(cls,cursor,email, password):
        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()

        if user:
            return cls(*user)
        else:
            return None
