from os import getenv

class SQLServerConfig:
    SERVER = getenv('MSSQL_SERVER')
    DB = getenv('MSSQL_DB')
    DRIVER = getenv('MSSQL_DRIVER')
    TRUSTED_CONNECTION = "yes"  # Para Windows Authentication

class MySQLConfig:
    HOST = getenv('MYSQL_HOST')
    USER = getenv('MYSQL_USER')
    PASSWORD = getenv('MYSQL_PASSWORD')
    DB = getenv('MYSQL_DB')
