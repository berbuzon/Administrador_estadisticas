from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import sessionmaker
from src.database.conexiones import conectar_sqlserver, conectar_mysql
from src.demo.demo_manual import demostrar_modelos_manuales

# Crear conexiones
engine_sql = conectar_sqlserver()
engine_mysql = conectar_mysql()

# Crear sesiones
SessionSQL = sessionmaker(bind=engine_sql)
SessionMySQL = sessionmaker(bind=engine_mysql)
