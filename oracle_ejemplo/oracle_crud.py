from datetime import datetime
import os
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

def create_all_tables():
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

def update_departamento(
    id,
    nombre: Optional[str] = None,
    fecha_creacion: Optional[str] = None
):
    modificaciones = []
    parametros = {"id": id}

    if nombre is not None:
        modificaciones.append("nombre =: nombre")
        parametros["nombre"] = nombre
    if fecha_creacion is not None:
        modificaciones.append("fecha_creacion =: fecha_creacion")
        parametros["fecha_creacion"] = datetime.strptime(
            fecha_creacion, "%Y-%m-%d")
    if not modificaciones:
        return print("No hay campos para actualizar.")

    sql = f"UPDATE departamentos SET {", ".join(modificaciones)} WHERE id =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Departamento con ID={id} actualizado.")

def update_empleado(
    id,
    sueldo: Optional[int] = None,
    idPersona: Optional[int] = None,
    idDepartamento: Optional[int] = None
):
    modificaciones = []
    parametros = {"id": id}

    if sueldo is not None:
        modificaciones.append("sueldo =: sueldo")
        parametros["sueldo"] = sueldo
    if idPersona is not None:
        modificaciones.append("idPersona =: idPersona")
        parametros["idPersona"] = idPersona
    if idDepartamento is not None:
        modificaciones.append("idDepartamento =: idDepartamento")
        parametros["idDepartamento"] = idDepartamento
    if not modificaciones:
        return print("No hay campos para actualizar.")

    sql = f"UPDATE empleados SET {", ".join(modificaciones)} WHERE id =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Empleado con ID={id} actualizado.")

# Delete - Eliminación de datos
def delete_persona(id: int):
    sql = (
        "DELETE FROM PERSONAS WHERE id = :id"
    )

    parametros = {"id" : id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar dato: {err} \n {sql} \n {parametros}")

def delete_departamento(id: int):
    sql = (
        "DELETE FROM DEPARTAMENTOS WHERE id = :id"
    )

    parametros = {"id" : id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar dato: {err} \n {sql} \n {parametros}")
    
def delete_empleado(id: int):
    sql = (
        "DELETE FROM EMPLEADOS WHERE id = :id"
    )

    parametros = {"id" : id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar dato: {err} \n {sql} \n {parametros}")


def menu_personas():
    while True:
        os.system("cls")
        print(
            """
            ==========================================
            |         ⚆_⚆ Menú Personas             |
            ==========================================
            | 1. Insertar personas                   |
            | 2. Leer personas                       |
            | 3. Leer persona por ID                 |
            | 4. Modificar personas                  |
            | 5. Eliminar personas                   |
            | 0. Volver al menú principal            |
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-5, 0 para volver al menu principal]:")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id = int(input("Ingrese el id numerico de la persona: "))
                rut = input("Ingresa el rut sin puntos ni digito verificador. Ej: 12345678: ")
                nombres = input("Ingrese nombres de la persona: ")
                apellidos = input("Ingrese apellidos de la persona: ")
                fecha_nacimiento = input("Ingresa la fecha de nacimiento (año-mes-dia). Ej: 2002-12-30: ")
                create_persona(id,rut,nombres,apellidos,fecha_nacimiento)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_personas()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id = int(input("Ingrese el id numerico de la persona: "))
                read_persona_by_id(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id = int(input("Ingrese el id numerico de la persona: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                rut = input("Ingresa el rut sin puntos ni digito verificador. Ej: 12345678: ")
                nombres = input("Ingrese nombres de la persona: ")
                apellidos = input("Ingrese apellidos de la persona: ")
                fecha_nacimiento = input("Ingresa la fecha de nacimiento (año-mes-dia). Ej: 2002-12-30: ")
                if len(rut.strip()) == 0:
                    rut = None
                if len(nombres.strip()) == 0:
                    nombres = None
                if len(apellidos.strip()) == 0:
                    apellidos = None
                if len(fecha_nacimiento.strip()) == 0:
                    fecha_nacimiento = None
                update_persona(id,rut,nombres,apellidos,fecha_nacimiento)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id = int(input("Ingrese el id numerico de la persona: "))
                delete_persona(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break

def main():
    while True:
        os.system("cls")
        print(
            """
            ==========================================
            |         ⚆_⚆ CRUD CON ORACLESQL        |
            ==========================================
            | 1. APLICAR ESQUEMA EN LA BASE DE DATOS |
            | 2. TABLA PERSONAS                      |
            | 3. TABLA DEPARTAMENTOS                 |
            | 4. TABLA EMPLEADOS                     |
            | 0. SALIR                               |
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-4, 0 para salir]:")

        if opcion == "0":
            print("Adios ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            create_all_tables()
            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            menu_personas()
        elif opcion == "3":
            pass
        elif opcion == "4":
            pass
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break

if __name__ == "__main__":
    main()