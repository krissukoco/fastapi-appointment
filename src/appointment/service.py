from psycopg2.extensions import connection
from typing import Optional, List
from ulid import ULID

from src.appointment.model import Appointment
from src.database.postgres import DB
from src.utils.common import current_timestamp

def migrate_appointment(conn: connection) -> None:
    q = """
        CREATE TABLE IF NOT EXISTS appointments (
            id VARCHAR(255) PRIMARY KEY,
            organization_id VARCHAR(255) NOT NULL,
            apointee_id VARCHAR(255) NOT NULL,
            service_id VARCHAR(255) NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            customer_name VARCHAR(255) NOT NULL,
            customer_phone VARCHAR(255),
            customer_email VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            start_at BIGINT NOT NULL,
            end_at BIGINT NOT NULL,
            status VARCHAR(255) NOT NULL,
            price INT NOT NULL,
            paid BOOLEAN DEFAULT FALSE,
            created_at BIGINT NOT NULL,
            updated_at BIGINT NOT NULL
        );
    """
    cur = conn.cursor()
    cur.execute(q)
    conn.commit()
    cur.close()
migrate_appointment(DB)

def _appointment_from_row(row) -> Appointment:
    return Appointment(
        id=row[0],
        organization_id=row[1],
        apointee_id=row[2],
        service_id=row[3],
        user_id=row[4],
        customer_name=row[5],
        customer_phone=row[6] if row[6] is not None else "",
        customer_email=row[7],
        title=row[8],
        start_at=row[9],
        end_at=row[10],
        status=row[11],
        price=row[12],
        paid=row[13],
        created_at=row[14],
        updated_at=row[15],
    )

def _appointment_rows() -> List[str]:
    return list(Appointment.__fields__.keys())

def _appointment_sql_rows() -> str:
    return ", ".join(_appointment_rows())

def new_appointment_id() -> str:
    return "a_" + str(ULID())

def get_appointment_by_id(id: str) -> Optional[Appointment]:
    q = f"""SELECT {_appointment_sql_rows()}
        FROM appointments WHERE id = '{id}';
    """
    cur = DB.cursor()
    cur.execute(q)
    appointment = cur.fetchone()
    cur.close()
    if appointment is None:
        return None
    return _appointment_from_row(appointment)

def get_appointments_by_organization(organization_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> list[Appointment]:
    if page is None:
        page = 1
    if limit is None:
        limit = 10
    q = f"""SELECT {_appointment_sql_rows()}
        FROM appointments WHERE organization_id = '{organization_id}' ORDER BY created_at DESC
        LIMIT {limit} OFFSET {(page-1) * limit};
    """
    cur = DB.cursor()
    cur.execute(q)
    res = cur.fetchall()
    cur.close()
    return [ _appointment_from_row(row) for row in res ]

def create_appointment(data: Appointment) -> None:
    data.id = new_appointment_id()
    ts = current_timestamp()
    data.created_at = ts
    data.updated_at = ts
    q = f"""INSERT INTO appointments ({_appointment_sql_rows()}) VALUES (
        '{data.id}',
        '{data.organization_id}',
        '{data.apointee_id}',
        '{data.service_id}',
        '{data.user_id}',
        '{data.customer_name}',
        '{data.customer_phone}',
        '{data.customer_email}',
        '{data.title}',
        {data.start_at},
        {data.end_at},
        '{data.status}',
        {data.price},
        {data.paid},
        {data.created_at},
        {data.updated_at}
    );"""
    cur = DB.cursor()
    cur.execute(q)
    DB.commit()
    cur.close()

def update_apppointment(data: Appointment) -> None:
    data.updated_at = current_timestamp()
    q = f"""UPDATE appointments SET
        organization_id = '{data.organization_id}',
        apointee_id = '{data.apointee_id}',
        service_id = '{data.service_id}',
        user_id = '{data.user_id}',
        customer_name = '{data.customer_name}',
        customer_phone = '{data.customer_phone}',
        customer_email = '{data.customer_email}',
        title = '{data.title}',
        start_at = {data.start_at},
        end_at = {data.end_at},
        status = '{data.status}',
        price = {data.price},
        paid = {data.paid},
        updated_at = {data.updated_at}
        WHERE id = '{data.id}';
    """
    cur = DB.cursor()
    cur.execute(q)
    DB.commit()
    cur.close()