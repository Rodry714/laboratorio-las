import sqlite3

conexion = sqlite3.connect("usuarios.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    correo TEXT,
    password TEXT
);
""")

conexion.commit()
conexion.close()

print("Base de datos y tabla creada correctamente.")  