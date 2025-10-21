from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import sessionmaker
from src.database.conexiones import conectar_sqlserver, conectar_mysql
from src.demo.demo_manual import demostrar_modelos_manuales

# Crear conexiones
engine_sql = conectar_sqlserver()
engine_mysql = conectar_mysql()

# Crear clases de sesión
SessionSQL = sessionmaker(bind=engine_sql)
SessionMySQL = sessionmaker(bind=engine_mysql)

# Crear instancias de sesión
session_sql = SessionSQL()
session_mysql = SessionMySQL()

if __name__ == "__main__":
    print("Iniciando demostración de modelos manuales...")
    demostrar_modelos_manuales(session_sql, session_mysql)
    print("Demostración completada.")

    # Cerrar sesiones al final
    session_sql.close()
    session_mysql.close()

