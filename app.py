import sqlite3
from flask import Flask, flash, render_template, request, redirect, url_for, session
from models.admin import admin
from models.alumno import alumno
from models.entrenador import entrenador
from models.usuario import usuario
from database.database import create_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    if app.config.get('TESTING'):
        return sqlite3.connect(':memory:')
    return create_connection()

#Ruta para la página principal
@app.route('/')
def home():
    if 'user_id' in session:
        if session['user_type'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session['user_type'] == 'entrenador':
            return redirect(url_for('entrenador_dashboard'))
        elif session['user_type'] == 'alumno':
            return redirect(url_for('alumno_dashboard'))
    return render_template('login.html')

# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = create_connection()
        cursor = conn.cursor()

        user = usuario.login(cursor, email, password)

        conn.close()

        if user:
            session['user_id'] = user.id
            session['user_type'] = user.tipo_usuario
            if user.tipo_usuario == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.tipo_usuario == 'entrenador':
                return redirect(url_for('entrenador_dashboard'))
            elif user.tipo_usuario == 'alumno':
                return redirect(url_for('alumno_dashboard'))
        else:
            return "credenciales de login incorretas!"
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

# Ruta para el dashboard de admin
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' in session and session['user_type'] == 'admin':
        conn = create_connection()
        cursor = conn.cursor()
    
        rutinas = admin.get_all_rutinas(cursor)
        cursor.close()
        conn.close()
        return render_template('admin_dashboard.html', rutinas=rutinas)
    else:
        return redirect(url_for('login'))
    
# Ruta para editar rutina
@app.route('/edit_rutina/<int:rutina_id>', methods=['GET', 'POST'])
def edit_rutina(rutina_id):
    if 'user_id' in session and session['user_type'] in ['admin', 'entrenador']:
        conn = create_connection()
        cursor = conn.cursor()

        # Obtener la rutina por ID
        rutina = None
        if session['user_type'] == 'admin':
            rutina = admin.get_rutina_by_id(cursor, rutina_id)
        elif session['user_type'] == 'entrenador':
            rutina = entrenador.get_rutina_by_id(cursor, rutina_id)

        cursor.close()
        conn.close()

        if rutina:
            if request.method == 'POST':
                nombre_ejercicio = request.form['nombre_ejercicio']
                descripcion = request.form['descripcion']

                conn = create_connection()
                cursor = conn.cursor()

                if session['user_type'] == 'admin':
                    admin.update_rutina(cursor, rutina_id, nombre_ejercicio, descripcion)
                elif session['user_type'] == 'entrenador':
                    entrenador.update_rutina(cursor, rutina_id, nombre_ejercicio, descripcion)

                conn.commit()
                conn.close()

                flash('Rutina actualizada correctamente', 'success')
                return redirect(url_for('entrenador_dashboard' if session['user_type'] == 'entrenador' else 'admin_dashboard'))
            else:
                return render_template('edit_rutina.html', rutina=rutina)
        else:
            flash('Rutina no encontrada', 'error')
            return redirect(url_for('entrenador_dashboard' if session['user_type'] == 'entrenador' else 'admin_dashboard'))
    else:
        return redirect(url_for('login'))
# Ruta para eliminar rutina
@app.route('/delete_rutina/<int:rutina_id>')
def delete_rutina(rutina_id):
    if 'user_id' in session and session['user_type'] in ['admin', 'entrenador']:
        conn = create_connection()
        cursor = conn.cursor()

        if session['user_type'] == 'admin':
            admin.delete_rutina(cursor, rutina_id)
        elif session['user_type'] == 'entrenador':
            entrenador.delete_rutina(cursor, rutina_id)

        conn.commit()
        conn.close()

        flash('Rutina eliminada correctamente', 'success')
        return redirect(url_for('entrenador_dashboard' if session['user_type'] == 'entrenador' else 'admin_dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/entrenador/dashboard')
def entrenador_dashboard():
    if 'user_id' in session and session['user_type'] == 'entrenador':
        conn = create_connection()
        cursor = conn.cursor()
    
        entrenador_actual = entrenador.get_by_id(cursor, session['user_id'])  # Aquí se pasa el user_id
        
        if entrenador_actual:
            rutinas = entrenador_actual.get_rutinas()
            cursor.close()
            conn.close()
            return render_template('entrenador_dashboard.html', rutinas=rutinas)
        else:
            cursor.close()
            conn.close()
            flash('Entrenador no encontrado.', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
@app.route('/entrenador/asignar_rutina', methods=['POST'])
def asignar_rutina():
    if 'user_id' in session and session['user_type'] == 'entrenador':
        if request.method == 'POST':
            entrenador_id = session['user_id']
            alumno_id = request.form.get('alumno_id')
            nombre_ejercicio = request.form.get('nombre_ejercicio')
            descripcion = request.form.get('descripcion')

            entrenador.assign_rutina_to_alumno(entrenador_id, alumno_id, nombre_ejercicio, descripcion)

            flash('Rutina asignada correctamente al alumno.', 'success')
            return redirect(url_for('entrenador_dashboard'))
        else:
            conn = create_connection()
            cursor = conn.cursor()

            # Obtener la lista de alumnos
            cursor.execute("SELECT id, nombre FROM usuarios WHERE tipo_usuario = 'alumno'")
            alumnos = cursor.fetchall()
            conn.close()

            return render_template('asignar_rutina.html', alumnos=alumnos)
    else:
        return redirect(url_for('login'))

@app.route('/alumno/dashboard')
def alumno_dashboard():
    if 'user_id' in session and session['user_type'] == 'alumno':
        conn = create_connection()
        cursor = conn.cursor()

        # Obtener datos del alumno desde la base de datos
        alumno_actual = alumno.get_by_id(cursor, session['user_id'])

        if alumno_actual:
            rutinas = alumno_actual.get_assigned_rutinas()
            entrenador = alumno_actual.get_entrenador()
            cursor.close()
            conn.close()
            return render_template('alumno_dashboard.html', rutinas=rutinas, entrenador=entrenador)
        else:
            cursor.close()
            conn.close()
            flash('Alumno no encontrado.', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    
@app.route('/agregar_rutina', methods=['GET', 'POST'])
def agregar_rutina():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre_ejercicio = request.form['nombre_ejercicio']
        descripcion = request.form['descripcion']

        if not nombre_ejercicio or not descripcion:
            flash('Todos los campos son obligatorios.')
            return redirect(url_for('agregar_rutina'))

        # Obtener el entrenador actual desde la base de datos usando el user_id de la sesión
        conn = sqlite3.connect('database/fitpal.db')
        cursor = conn.cursor()
        entrenador_actual = entrenador.get_by_id(cursor, session['user_id'])
        conn.close()

        if entrenador_actual:
            # Agregar la rutina a través del método de la clase entrenador
            entrenador_actual.add_rutina(nombre_ejercicio, descripcion)
            flash('Rutina agregada exitosamente.')
            return redirect(url_for('entrenador_dashboard'))
        else:
            flash('No se encontró al entrenador.')
            return redirect(url_for('agregar_rutina'))
    
    return render_template('agregar_rutina.html')

if __name__ == '__main__':
    app.run(debug=True)
