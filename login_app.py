from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import os

app = Flask(__name__)
DB_NAME = 'usuarios.db'

# Crea la base de datos y la tabla si no existe
def crear_base_datos():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('CREATE TABLE usuarios (nombre TEXT, password TEXT)')
        conn.commit()
        conn.close()

# Función para agregar usuarios con contraseña en hash SHA256
def agregar_usuario(nombre, password_plano):
    hash_password = hashlib.sha256(password_plano.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO usuarios (nombre, password) VALUES (?, ?)', (nombre, hash_password))
    conn.commit()
    conn.close()

# Lista de integrantes del examen
integrantes = {
    "Matias": "clave123",
    "Esteban": "abc456"
}

# Crear la base de datos y cargar los usuarios
crear_base_datos()
for nombre, clave in integrantes.items():
    agregar_usuario(nombre, clave)

# HTML del login
html_login = """
<h2>Ingreso de Usuario</h2>
<form method="POST">
  Nombre de usuario: <input name="usuario"><br>
  Contraseña: <input name="clave" type="password"><br>
  <input type="submit" value="Ingresar">
</form>
{% if mensaje %}
<p>{{ mensaje }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        hash_clave = hashlib.sha256(clave.encode()).hexdigest()

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (usuario, hash_clave))
        result = c.fetchone()
        conn.close()

        if result:
            mensaje = "✅ Acceso concedido. Bienvenido, " + usuario + "."
        else:
            mensaje = "❌ Usuario o contraseña incorrecta."
    return render_template_string(html_login, mensaje=mensaje)

if __name__ == "__main__":
    app.run(port=5800)
