import os
import sys
from datetime import datetime
from typing import Optional, List, Dict, Any

import oracledb
from dotenv import load_dotenv

load_dotenv()

ORACLE_USER = os.getenv("ORACLE_USER", "scott")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost/orclpdb")

if ORACLE_PASSWORD is None:
    print("AVISO: la variable de entorno ORACLE_PASSWORD no está definida. Establezca ORACLE_PASSWORD para conectar.")


def get_connection():
    return oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)


def create_table() -> None:
    ddl = (
        "CREATE TABLE personas ("
        "rut VARCHAR2(50) PRIMARY KEY,"
        "nombres VARCHAR2(200),"
        "apellidos VARCHAR2(200),"
        "fecha_nacimiento DATE,"
        "cod_area VARCHAR2(20),"
        "numero_telefono VARCHAR2(50)"
        ")"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(ddl)
                print("Tabla 'personas' creada.")
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la tabla: {err}")


def create_persona(rut: str, nombres: str, apellidos: str, fecha_nacimiento: Optional[str], cod_area: str, numero_telefono: str) -> None:
    sql = (
        "INSERT INTO personas (rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono) "
        "VALUES (:rut, :nombres, :apellidos, :fecha_nacimiento, :cod_area, :numero_telefono)"
    )
    bind_fecha = None
    if fecha_nacimiento:
        bind_fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {
                "rut": rut,
                "nombres": nombres,
                "apellidos": apellidos,
                "fecha_nacimiento": bind_fecha,
                "cod_area": cod_area,
                "numero_telefono": numero_telefono,
            })
            conn.commit()
            print(f"Persona con RUT={rut} creada.")


def read_persona(rut: str) -> Optional[Dict[str, Any]]:
    sql = "SELECT rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono FROM personas WHERE rut = :rut"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"rut": rut})
            row = cur.fetchone()
            if not row:
                return None
            rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono = row
            return {
                "rut": rut,
                "nombres": nombres,
                "apellidos": apellidos,
                "fecha_nacimiento": fecha_nacimiento.isoformat() if fecha_nacimiento else None,
                "cod_area": cod_area,
                "numero_telefono": numero_telefono,
            }


def list_personas(limit: int = 100) -> List[Dict[str, Any]]:
    sql = f"SELECT rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono FROM personas FETCH FIRST {limit} ROWS ONLY"
    results = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            for row in cur:
                rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono = row
                results.append({
                    "rut": rut,
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "fecha_nacimiento": fecha_nacimiento.isoformat() if fecha_nacimiento else None,
                    "cod_area": cod_area,
                    "numero_telefono": numero_telefono,
                })
    return results


def update_persona(rut: str, nombres: Optional[str] = None, apellidos: Optional[str] = None, fecha_nacimiento: Optional[str] = None, cod_area: Optional[str] = None, numero_telefono: Optional[str] = None) -> None:
    sets = []
    binds = {"rut": rut}
    if nombres is not None:
        sets.append("nombres = :nombres")
        binds["nombres"] = nombres
    if apellidos is not None:
        sets.append("apellidos = :apellidos")
        binds["apellidos"] = apellidos
    if fecha_nacimiento is not None:
        sets.append("fecha_nacimiento = :fecha_nacimiento")
        binds["fecha_nacimiento"] = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    if cod_area is not None:
        sets.append("cod_area = :cod_area")
        binds["cod_area"] = cod_area
    if numero_telefono is not None:
        sets.append("numero_telefono = :numero_telefono")
        binds["numero_telefono"] = numero_telefono

    if not sets:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE personas SET " + ", ".join(sets) + " WHERE rut = :rut"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, binds)
            conn.commit()
            print(f"Persona con RUT={rut} actualizada.")


def delete_persona(rut: str) -> None:
    sql = "DELETE FROM personas WHERE rut = :rut"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"rut": rut})
            conn.commit()
            print(f"Persona con RUT={rut} eliminada (si existía).")
