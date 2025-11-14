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

for query in tables:
    create_schema(query)


# PERSONAS
# Create - Inserción de datos
from datetime import datetime
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
        "fecha_nacimiento": datetime.strptime(fecha_nacimiento,"%Y-%m-%d")
    }

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql,parametros)
                print(f"Dato insertado \n {parametros}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err} \n {parametros}")

create_persona(
    id=1,
    rut="19456321",
    nombres="Alejandra Maria",
    apellidos="Mayorga Cayuqueo",
    fecha_nacimiento="1998-08-30"
)


def create_departamento(
        id: int,
        nombre: str,
        fecha_creacion: str
):
    pass

def create_empleado(
        id: int,
        sueldo: int,
        idPersona: int,
        idDepartamento: int
):
    pass
