from sqlalchemy import create_engine
from config.settings import SQLServerConfig, MySQLConfig
# from sqlalchemy import text  # Necesario para ejecutar queries

def conectar_sqlserver():
    # Construye la cadena de conexión para SQL Server usando f-strings
    connection_string = (
        f"mssql+pyodbc://{SQLServerConfig.SERVER}/{SQLServerConfig.DB}?"
        f"driver={SQLServerConfig.DRIVER.replace(' ', '+')}&"
        f"trusted_connection={SQLServerConfig.TRUSTED_CONNECTION}"
    )
    # Crea y retorna un motor SQLAlchemy con la cadena de conexión
    return create_engine(connection_string)

def conectar_mysql():
    # Conexión MySQL con parámetros optimizados
    engine = create_engine(
        f"mysql+pymysql://{MySQLConfig.USER}:{MySQLConfig.PASSWORD}@{MySQLConfig.HOST}/{MySQLConfig.DB}",
        pool_size=5,
        pool_recycle=3600,
        connect_args={
            'connect_timeout': 10,
            'charset': 'utf8mb4'
        }
    )
    return engine
