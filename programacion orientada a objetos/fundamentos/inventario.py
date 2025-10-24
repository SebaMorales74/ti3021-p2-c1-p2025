import os

class Producto:
    def __init__(self, nombre: str, stock: int):
        self.nombre: str = nombre
        self.stock: int = stock

    def __str__(self):
        return f"Producto: {self.nombre} 🔗 Stock actual:{self.stock}"


inventario: list[Producto] = []


def agregarProducto():
    nombre: str = input("Ingrese el nombre del producto: ")
    stockInicial: int = int(input("Ingrese el stock en formato numerico entero: "))
    producto: Producto = Producto(nombre=nombre, stock=stockInicial)
    inventario.append(producto)

def listarProducto():
    if len(inventario) <= 0:
        print("No hay productos")
        return
    
    for producto in inventario:
        print(producto)


while True:
    os.system('cls')
    print("""
            ============================================
                    Sistema de inventariado
            ============================================
                1. Listar inventario
                2. Crear producto
                3. Salir
            ============================================       
          """)
    opcion = int(input("Ingresa una opción [1-3]: "))
    if opcion == 1:
        os.system('cls')
        listarProducto()
        input("Ingrese ENTER para continuar....\n")
    elif opcion == 2:
        os.system('cls')
        agregarProducto()
        input("Ingrese ENTER para continuar....\n")
    elif opcion == 3:
        os.system('cls')
        input("Ingrese ENTER para salir....\n")
        break
    else:
        os.system('cls')
        print("Opción incorrecta, ingrese nuevamente.")
        input("Ingrese ENTER para continuar....\n")
