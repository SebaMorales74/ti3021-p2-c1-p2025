class Mascotas:
    def __init__(self, nombre: str, edad: int, especie: str):
        self._nombre: str = nombre
        self._edad: int = edad
        self._especie: str = especie


class Perro:
    def __init__(self):
        self.__historial_de_vacunas: list[dict] = []


class Gato:
    def __init__(self):
        self.__registro_de_estirilizacion: str = ""


class Ave:
    def __init__(self):
        self.__control_de_vuelo: list[dict] = []
        self.__jaula: str = ""
