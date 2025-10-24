class Carro:
    def __init__(self, modelo: str, color: str):
        self.modelo: str = modelo
        self.color: str = color

    @classmethod
    def mercedes_benz(cls):
        return cls("Mercedes Benz", "Blanco")

    def __str__(self):
        return f"{self.modelo} {self.color}"


# auto1 = Carro(modelo="Chevrolet Spark", color="Azul marino")
auto1 = Carro.mercedes_benz()
print(auto1)