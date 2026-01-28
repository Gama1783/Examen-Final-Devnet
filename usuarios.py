import sqlite3
import hashlib
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Ruta fija para asegurar que se use el archivo correcto
conn = sqlite3.connect("/home/devasc/examen_final/usuarios.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL
)
""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/")
def home():
    return render_template_string("""
        <h1>Gestión de Usuarios</h1>
        <h2>Registrar Usuario</h2>
        <form action="/registrar_web" method="post">
            Usuario: <input type="text" name="usuario"><br>
            Password: <input type="password" name="password"><br>
            Rol: <input type="text" name="rol"><br>
            <input type="submit" value="Registrar">
        </form>
        <h2>Login</h2>
        <form action="/login_web" method="post">
            Usuario: <input type="text" name="usuario"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    """)

@app.route("/registrar_web", methods=["POST"])
def registrar_web():
    usuario = request.form.get("usuario")
    password = request.form.get("password")
    rol = request.form.get("rol")
    if not usuario or not password or not rol:
        return "<p>Faltan datos</p><form action='/'><input type='submit' value='Volver'></form>"

    password_hash = hash_password(password)
    try:
        cursor.execute("INSERT INTO usuarios (usuario, password_hash, rol) VALUES (?, ?, ?)", 
                       (usuario, password_hash, rol))
        conn.commit()
        return f"<p>Usuario {usuario} registrado como {rol}</p><form action='/'><input type='submit' value='Volver'></form>"
    except sqlite3.IntegrityError:
        return "<p>Usuario ya existe</p><form action='/'><input type='submit' value='Volver'></form>"

@app.route("/login_web", methods=["POST"])
def login_web():
    usuario = request.form.get("usuario")
    password = request.form.get("password")
    password_hash = hash_password(password)

    cursor.execute("SELECT rol FROM usuarios WHERE usuario=? AND password_hash=?", (usuario, password_hash))
    result = cursor.fetchone()

    if result:
        return f"""
            <p>Bienvenido {usuario}, Rol: {result[0]}</p>
            <form action="/logout" method="get">
                <input type="submit" value="Salir">
            </form>
        """
    else:
        return "<p>Credenciales inválidas</p><form action='/'><input type='submit' value='Volver'></form>"

@app.route("/logout")
def logout():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800)