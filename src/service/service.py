from psycopg2.extensions import connection
from typing import Optional, List

from src.database.postgres import DB
from src.service.model import Service

def migrate_services(conn: connection) -> None:
    q = """
        CREATE TABLE IF NOT EXISTS services (
            id VARCHAR(255) PRIMARY KEY,
            organization_id VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            category VARCHAR(255),
            image TEXT,
            timezone VARCHAR(255) NOT NULL,
            start_time INT NOT NULL,
            end_time INT NOT NULL,
            duration INT NOT NULL,
            gap INT NOT NULL,
            break_time INT NOT NULL,
            break_duration INT NOT NULL,
            break_days TEXT,
            price INT NOT NULL,
            slot_per_session INT NOT NULL,
            created_at BIGINT NOT NULL,
            updated_at BIGINT NOT NULL
        );
    """
    cur = conn.cursor()
    cur.execute(q)
    conn.commit()
    cur.close()

migrate_services(DB)

def _service_from_row(row) -> Service:
    return Service(
        id=row[0],
        organization_id=row[1],
        title=row[2],
        description=row[3],
        category=row[4],
        image=row[5] if row[5] is not None else "",
        timezone=row[6],
        start_time=row[7],
        end_time=row[8],
        duration=row[9],
        gap=row[10],
        break_time=row[11],
        break_duration=row[12],
        break_days=row[13] if row[13] is not None else "",
        price=row[14],
        slot_per_session=row[15],
        created_at=row[16],
        updated_at=row[17],
    )

def _service_rows() -> List[str]:
    return list(Service.__fields__.keys())

def _service_sql_rows() -> str:
    return ", ".join(_service_rows())

def get_service_by_id(id: str) -> Optional[Service]:
    q = f"SELECT {_service_sql_rows()} FROM services WHERE id = '{id}' LIMIT 1;"
    cur = DB.cursor()
    cur.execute(q)
    res = cur.fetchone()
    cur.close()
    if res is None:
        return None
    return _service_from_row(res)

def get_services_by_organization_id(organization_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> List[Service]:
    if page is None:
        page = 1
    if limit is None:
        limit = 10

    q = f"""SELECT {_service_sql_rows()} FROM services WHERE organization_id = '{organization_id}'
        ORDER BY created_at DESC LIMIT {limit} OFFSET {(page - 1) * limit};
    """
    cur = DB.cursor()
    cur.execute(q)
    res = cur.fetchall()
    cur.close()
    return [ _service_from_row(r) for r in res ]