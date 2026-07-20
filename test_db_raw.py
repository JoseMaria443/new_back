import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(db_url)
    print("¡Conexión exitosa a la base de datos!")
    conn.close()
except Exception as e:
    print("--- ERROR REAL DE POSTGRESQL ---")
    if isinstance(e, UnicodeDecodeError) and len(e.args) > 1 and isinstance(e.args[1], bytes):
        print(e.args[1].decode('cp1252', errors='replace'))
    else:
        print(repr(str(e).encode('utf-8', 'replace')))
