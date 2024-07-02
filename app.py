from flask import Flask, flash, render_template, request, redirect, url_for, session
from models.admin import admin
from models.alumno import alumno
from models.entrenador import entrenador
from models.usuario import usuario
from database.database import create_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'


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
    if 'user_id' in session and session['user_type'] == 'admin':
        conn = create_connection()
        cursor = conn.cursor()

        rutina = admin.get_rutina_by_id(cursor, rutina_id)

        cursor.close()
        conn.close()

        if rutina:
            if request.method == 'POST':
                # Procesar la actualización de la rutina aquí si es necesario
                flash('Rutina actualizada correctamente', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('edit_rutina.html', rutina=rutina)
        else:
            flash('Rutina no encontrada', 'error')
            return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))

# Ruta para eliminar rutina
@app.route('/delete_rutina/<int:rutina_id>')
def delete_rutina(rutina_id):
    if 'user_id' in session and session['user_type'] == 'admin':
        conn = create_connection()
        cursor = conn.cursor()

        admin.delete_rutina(cursor, rutina_id)

        conn.commit()  # Aplica los cambios a la base de datos
        conn.close()
        
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/entrenador/dashboard')
def entrenador_dashboard():
    if 'user_id' in session and session['user_type'] == 'entrenador':
        entrenador_actual = entrenador.get_by_id(session['user_id'])  
        if entrenador_actual:
            rutinas = entrenador_actual.get_rutinas()
            return render_template('entrenador_dashboard.html', rutinas=rutinas)
        else:
            flash('Entrenador no encontrado.', 'error')
            return redirect(url_for('login'))
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
    if 'user_id' in session and session['user_type'] == 'entrenador':
        if request.method == 'POST':
            nombre_ejercicio = request.form['nombre_ejercicio']
            descripcion = request.form['descripcion']
            entrenador(session['user_id']).agregar_rutina(session['user_id'], nombre_ejercicio, descripcion)
            return redirect(url_for('entrenador_dashboard'))

        return render_template('agregar_rutina.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
