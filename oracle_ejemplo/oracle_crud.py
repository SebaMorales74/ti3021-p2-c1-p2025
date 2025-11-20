from datetime import datetime
import oracledb
import os
from dotenv import load_dotenv
load_dotenv()
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")


def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)


def create_schema(query):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                print(f"Tabla creada \n {query}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la tabla: {err} \n {query}")


tables = [
    (
        "CREATE TABLE personas ("
        "id INTEGER PRIMARY KEY,"
        "rut NUMBER(8),"
        "nombres VARCHAR(64),"
        "apellidos VARCHAR(64),"
        "fecha_nacimiento DATE"
        ")"
    ),
    (
        "CREATE TABLE departamentos ("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(32),"
        "fecha_creacion DATE"
        ")"
    ),
    (
        "CREATE TABLE empleados ("
        "id INTEGER PRIMARY KEY,"
        "sueldo NUMBER(10,2),"
        "idPersona INTEGER,"
        "idDepartamento INTEGER,"
        "FOREIGN KEY (idPersona) REFERENCES PERSONAS(id),"
        "FOREIGN KEY (idDepartamento) REFERENCES DEPARTAMENTOS(id)"
        ")"
    )
]

# for query in tables:
#     create_schema(query)


# PERSONAS
# Create - Inserción de datos


def create_persona(
        id: int,
        rut: str,
        nombres: str,
        apellidos: str,
        fecha_nacimiento: str
):
    sql = (
        "INSERT INTO PERSONAS (id, rut, nombres, apellidos, fecha_nacimiento)"
        "VALUES (:id,:rut,:nombres,:apellidos,:fecha_nacimiento)"
    )

    parametros = {
        "id": id,
        "rut": rut,
        "nombres": nombres,
        "apellidos": apellidos,
        "fecha_nacimiento": datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    }

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                print(f"Dato insertado \n {parametros}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err} \n {parametros}")


def create_departamento(
        id: int,
        nombre: str,
        fecha_creacion: str
):
    sql = (
        "INSERT INTO DEPARTAMENTOS (id, nombre, fecha_creacion)"
        "VALUES (:id,:nombre,:fecha_creacion)"
    )

    parametros = {
        "id": id,
        "nombre": nombre,
        "fecha_creacion": datetime.strptime(fecha_creacion, "%Y-%m-%d")
    }

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                print(f"Dato insertado \n {parametros}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err} \n {parametros}")


def create_empleado(
        id: int,
        sueldo: int,
        idPersona: int,
        idDepartamento: int
):
    sql = (
        "INSERT INTO EMPLEADOS (id, sueldo, idPersona, idDepartamento)"
        "VALUES (:id,:sueldo,:idPersona,:idDepartamento)"
    )

    parametros = {
        "id": id,
        "sueldo": sueldo,
        "idPersona": idPersona,
        "idDepartamento": idDepartamento
    }

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                print(f"Dato insertado \n {parametros}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err} \n {parametros}")


# Read - Consulta de datos
def read_personas():
    sql = (
        "SELECT * FROM PERSONAS"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print(f"Consulta a la tabla PERSONAS")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")


def read_persona_by_id(id):
    sql = (
        "SELECT * FROM PERSONAS WHERE id = :id"
    )

    parametros = {"id": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql, parametros)
                print(f"Consulta a la tabla PERSONAS por ID")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")


def read_departamentos():
    pass


def read_departamento_by_id(id):
    pass


def read_empleados():
    pass


def read_empleado_by_id(id):
    pass


# Update - Modificacion de datos

from typing import Optional
def update_persona(
    id,
    rut: Optional[str] = None,
    nombres: Optional[str] = None,
    apellidos: Optional[str] = None,
    fecha_nacimiento: Optional[str] = None
):
    modificaciones = []
    parametros = {"id": id}

    if rut is not None:
        modificaciones.append("rut =: rut")
        parametros["rut"] = rut
    if nombres is not None:
        modificaciones.append("nombres =: nombres")
        parametros["nombres"] = nombres
    if apellidos is not None:
        modificaciones.append("apellidos =: apellidos")
        parametros["apellidos"] = apellidos
    if fecha_nacimiento is not None:
        modificaciones.append("fecha_nacimiento =: fecha_nacimiento")
        parametros["fecha_nacimiento"] = datetime.strptime(
            fecha_nacimiento, "%Y-%m-%d")
    if not modificaciones:
        return print("No hay campos para actualizar.")

    sql = f"UPDATE personas SET {", ".join(modificaciones)} WHERE id =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Persona con RUT={rut} actualizada.")
