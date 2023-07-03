import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, find_dotenv
from os import getenv


env_file = find_dotenv()

load_dotenv(env_file)


DB_USERNAME = getenv("db_username")
DB_PASSWORD = getenv("db_password")
DB_HOST = getenv("db_host")
DB_PORT = getenv("db_port")
DB_NAME = getenv("db_name")


config = {
    'host': getenv("db_host"),
    'port': getenv("db_port"),
    'user': getenv("db_username"),
    'password': getenv("db_password")
}

try:
    conn = psycopg2.connect(**config,
                                 dbname="postgres",
                                 cursor_factory=RealDictCursor)
except Exception as e:
    print("DB Connection Error...")
    print(e)
    exit(1)

conn.autocommit = True

cursor = conn.cursor()
stmt = f'CREATE DATABASE {DB_NAME};'
cursor.execute(stmt)
cursor.execute('SELECT datname FROM pg_catalog.pg_database;')

for db in cursor:
    print(db)
