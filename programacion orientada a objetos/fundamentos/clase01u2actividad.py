"""
Aplicar completamente los siguietes pilares de la
Programacion Orientada a Objetos:
- Abstracción (Atributos y Metodos)
- Encapsulamiento (Visibilidad)
- Herencia (SuperClase, SubClase)
- Polimorfismo (DuckTyping)

"""

class Mascota:
    def __init__(self, nombre: str, edad: int, especie: str):
        self._nombre: str = nombre
        self._edad: int = edad
        self._especie: str = especie

    def emitirSonido(self,sonido):
        print(f"> {self._nombre} dijo {sonido}")

    @property
    def nombre(self):
        return self._nombre

    @property
    def edad(self):
        return self._edad

    @property
    def especie(self):
        return self._especie


class Perro(Mascota):
    def __init__(self, nombre: str, edad: int, especie: str):
        super().__init__(nombre=nombre, edad=edad, especie=especie)
        self.__historial_de_vacunas: list[dict] = []

    @property
    def historial_de_vacunas(self):
        return self.__historial_de_vacunas


class Gato(Mascota):
    def __init__(self):
        self.__registro_de_estirilizacion: str = ""

    @property
    def registro_de_estirilizacion(self):
        return self.__registro_de_estirilizacion


class Ave(Mascota):
    def __init__(self):
        self.__control_de_vuelo: list[dict] = []
        self.__jaula: str = ""

    @property
    def control_de_vuelo(self):
        return self.__control_de_vuelo

    @property
    def jaula(self):
        return self.__jaula


newPerro = Perro(
    nombre="Firulais",
    edad=7,
    especie="Poddle"
)

print(f"Nombre: {newPerro.nombre}\nEdad: {newPerro.edad}\nEspecie: {newPerro.especie}")
newPerro.emitirSonido("🐶 woof woof")