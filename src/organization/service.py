from typing import List, Optional
from psycopg2.extensions import connection
from ulid import ULID

from src.database.postgres import DB
from src.organization.model import Organization
from src.utils.common import current_timestamp

def migrate_organizations(conn: connection) -> None:
    q = """
        CREATE TABLE IF NOT EXISTS organizations (
            id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            image TEXT,
            address VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            country VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            phone VARCHAR(255),
            email VARCHAR(255),
            created_at BIGINT NOT NULL,
            updated_at BIGINT NOT NULL
        );
    """
    cur = conn.cursor()
    cur.execute(q)
    conn.commit()
    cur.close()

migrate_organizations(DB)

def _organization_from_row(row) -> Organization:
    return Organization(
        id=row[0],
        user_id=row[1],
        name=row[2],
        description=row[3],
        image=row[4] if row[4] is not None else "",
        address=row[5],
        city=row[6],
        country=row[7],
        category=row[8],
        phone=row[9] if row[9] is not None else "",
        email=row[10] if row[10] is not None else "",
        created_at=row[11],
        updated_at=row[12],
    )

def _organization_rows() -> List[str]:
    return list(Organization.__fields__.keys())

def _organization_sql_rows() -> str:
    return ", ".join(_organization_rows())

def new_organization_id() -> str:
    return "org_" + str(ULID())

def get_organization_by_id(id: str) -> Optional[Organization]:
    q = f"SELECT {_organization_sql_rows()} FROM organizations WHERE id = '{id}';"
    cur = DB.cursor()
    cur.execute(q)
    organization = cur.fetchone()
    cur.close()
    if organization is None:
        return None
    return _organization_from_row(organization)

def get_organization_by_user_id(user_id: str) -> Optional[Organization]:
    q = f"SELECT {_organization_sql_rows()} FROM organizations WHERE user_id = '{user_id}';"
    cur = DB.cursor()
    cur.execute(q)
    organization = cur.fetchone()
    cur.close()
    if organization is None:
        return None
    return _organization_from_row(organization)

def insert_organization(org: Organization) -> None:
    org.id = new_organization_id()
    org.created_at = org.updated_at = current_timestamp()

    q = f"""
        INSERT INTO organizations (
            {_organization_sql_rows()}
        ) VALUES (
            '{org.id}',
            '{org.user_id}',
            '{org.name}',
            '{org.description}',
            '{org.image}',
            '{org.address}',
            '{org.city}',
            '{org.country}',
            '{org.category}',
            '{org.phone}',
            '{org.email}',
            {org.created_at},
            {org.updated_at}
        );
    """
    cur = DB.cursor()
    cur.execute(q)
    DB.commit()
    cur.close()