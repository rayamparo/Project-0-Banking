import psycopg2
import os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Connection to db
def db_connection():
    host = os.getenv('host')
    database = os.getenv('database')
    user = os.getenv('user')
    password = os.getenv('password')
    return psycopg2.connect(
        host = f'{host}',
        database = f'{database}',
        user = f'{user}',
        password = f'{password}',
        port = 5432
    )