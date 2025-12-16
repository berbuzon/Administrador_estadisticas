from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import SQLServerConfig, MySQLConfig

# ==========================
# 1. Motores originales — NO se tocan
# ==========================

def conectar_sqlserver():
    connection_string = (
        f"mssql+pyodbc://{SQLServerConfig.SERVER}/{SQLServerConfig.DB}?"
        f"driver={SQLServerConfig.DRIVER.replace(' ', '+')}&"
        f"trusted_connection={SQLServerConfig.TRUSTED_CONNECTION}"
    )
    return create_engine(connection_string)

def conectar_mysql():
    engine = create_engine(
        f"mysql+pymysql://{MySQLConfig.USER}:{MySQLConfig.PASSWORD}"
        f"@{MySQLConfig.HOST}:3306/{MySQLConfig.DB}",
        pool_size=5,
        pool_recycle=3600,
        connect_args={
            'connect_timeout': 10,
            'charset': 'utf8mb4'
        }
    )
    return engine


# ==========================
# 2. Agregado para FastAPI + ORM
# ==========================

# Elegí acá el motor que la API va a usar
engine = conectar_mysql()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base ORM
Base = declarative_base()


# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
