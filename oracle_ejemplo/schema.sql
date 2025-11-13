CREATE TABLE
    PERSONAS (
        id INTEGER PRIMARY KEY,
        rut NUMBER (8),
        nombres VARCHAR(64),
        apellidos VARCHAR(64),
        fecha_nacimiento DATE
    );

CREATE TABLE
    DEPARTAMENTOS (
        id INTEGER PRIMARY KEY,
        nombre VARCHAR(32),
        fecha_creacion DATETIME
    );

CREATE TABLE
    EMPLEADOS (
        id INTEGER PRIMARY KEY,
        sueldo NUMBER (10, 2),
        idPersona INTEGER,
        idDepartamento INTEGER,
        FOREIGN KEY (idPersona) REFERENCES PERSONAS (id),
        FOREIGN KEY (idDepartamento) REFERENCES DEPARTAMENTOS (id)
    );