"""
Script Bulldozer para auto-creación de la base de datos comunicados_db.
Se conecta a la BD de mantenimiento 'postgres' y ejecuta CREATE DATABASE con autocommit.
Maneja errores de codificación CP1252/UTF-8 de Windows de forma segura.
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "postgres_root_pass")
target_db = os.getenv("DB_NAME", "comunicados_db")

print(f"🚜 Conectando a PostgreSQL ({host}:{port}) como usuario '{user}' en la BD 'postgres'...")

try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (target_db,))
    exists = cursor.fetchone()

    if not exists:
        print(f"⚙️ Creando la base de datos '{target_db}'...")
        cursor.execute(f'CREATE DATABASE "{target_db}" OWNER "{user}";')
        print(f"✅ ¡Base de datos '{target_db}' creada exitosamente!")
    else:
        print(f"ℹ️ La base de datos '{target_db}' ya existe.")

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Error de conexión/ejecución:")
    if isinstance(e, UnicodeDecodeError) and len(e.args) > 1 and isinstance(e.args[1], bytes):
        print(e.args[1].decode('cp1252', errors='replace'))
    else:
        try:
            print(repr(str(e).encode('utf-8', 'replace')))
        except Exception:
            print(repr(e))
