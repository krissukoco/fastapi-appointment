from typing import Optional, List
from ulid import ULID
from datetime import datetime
from psycopg2.extensions import connection

from src.database.postgres import DB
from src.user.model import User

def new_user_id() -> str:
    return "u_" + str(ULID())

def migrate_user(conn: connection) -> None:
    """
    Create user table in the database if not exists yet
    """
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY,
            organization_id VARCHAR(255),
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            image TEXT,
            role VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            created_at BIGINT NOT NULL,
            updated_at BIGINT NOT NULL
        );
    """)
    conn.commit()

def _user_from_row(row) -> User:
    return User(
        id=row[0],
        organization_id=row[1] if row[1] is not None else "",
        email=row[2],
        password=row[3],
        phone=row[4],
        first_name=row[5],
        last_name=row[6],
        image=row[7] if row[7] is not None else "",
        role=row[8],
        address=row[9] if row[9] is not None else "",
        created_at=row[10],
        updated_at=row[11]
    )

def _user_columns() -> List[str]:
    return list(User.__fields__.keys())

def _sql_user_columns() -> str:
    return ", ".join(_user_columns())

def get_user_by_id(id: str) -> Optional[User]:
    q = f"SELECT {_sql_user_columns()} FROM users WHERE id = '{id}';"
    cur = DB.cursor()
    cur.execute(q)
    user = cur.fetchone()
    cur.close()
    if user is None:
        return None
    return _user_from_row(user)

def get_user_by_email(email: str) -> Optional[User]:
    q = f"""SELECT {_sql_user_columns()} FROM users WHERE email = '{email}';"""
    cur = DB.cursor()
    cur.execute(q)
    user = cur.fetchone()
    print(user)
    cur.close()
    if user is None:
        return None
    return _user_from_row(user)

def get_user_by_id_and_organization(id: str, organization_id: str) -> Optional[User]:
    q = f"""SELECT {_sql_user_columns()} FROM users WHERE id = '{id}' AND organization_id = '{organization_id}';"""
    cur = DB.cursor()
    cur.execute(q)
    user = cur.fetchone()
    cur.close()
    if user is None:
        return None
    return _user_from_row(user)

def insert_user(user: User) -> None:
    now = int(datetime.utcnow().timestamp() * 1000)
    user.created_at = now
    user.updated_at = now
    user.id = new_user_id()
    q = f"""INSERT INTO users ({ _sql_user_columns() }) VALUES (
        '{user.id}',
        '{user.organization_id}',
        '{user.email}',
        '{user.password}',
        '{user.phone}',
        '{user.first_name}',
        '{user.last_name}',
        '{user.image}',
        '{user.role}',
        '{user.address}',
        {user.created_at},
        {user.updated_at}
    );"""
    cur = DB.cursor()
    cur.execute(q)
    DB.commit()

migrate_user(DB)

def update_user(user: User) -> None:
    now = int(datetime.utcnow().timestamp() * 1000)
    user.updated_at = now
    q = f"""UPDATE users SET
        organization_id = '{user.organization_id}',
        email = '{user.email}',
        password = '{user.password}',
        phone = '{user.phone}',
        first_name = '{user.first_name}',
        last_name = '{user.last_name}',
        image = '{user.image}',
        role = '{user.role}',
        address = '{user.address}',
        updated_at = {user.updated_at}
        WHERE id = '{user.id}';
    """
    cur = DB.cursor()
    cur.execute(q)
    DB.commit()