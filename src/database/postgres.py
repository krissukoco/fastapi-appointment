import os
import psycopg2
from ..exceptions.env import EnvNotSetException

def connect_default():
    env = os.environ

    if "POSTGRES_HOST" not in env:
        raise EnvNotSetException("POSTGRES_HOST")
    host = env["POSTGRES_HOST"]
    if "POSTGRES_DB" not in env:
        raise EnvNotSetException("POSTGRES_DB")
    db_name = env["POSTGRES_DB"]
    if "POSTGRES_USER" not in env:
        raise EnvNotSetException("POSTGRES_USER")
    user = env["POSTGRES_USER"]
    if "POSTGRES_PASSWORD" not in env:
        raise EnvNotSetException("POSTGRES_PASSWORD")
    password = env["POSTGRES_PASSWORD"]
    if "POSTGRES_PORT" not in env:
        raise EnvNotSetException("POSTGRES_PORT")
    port = int(env["POSTGRES_PORT"])

    conn = psycopg2.connect(
        host=host,
        database=db_name,
        user=user,
        password=password,
        port=port
    )
    return conn

DB = connect_default()