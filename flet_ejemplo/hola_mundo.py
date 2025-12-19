# Primer paso: Importar Flet
import flet as ft
# Segundo paso: Establecer la clase de mi aplicación
class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hola mundo"
        # Aplicar interfaz
        self.build()
    # Función de construcción de interfaz
    def build(self):
        self.page.add(
            ft.Text("Hola mundo")
        )
# Tercer paso: Ejecutar la apliación
if __name__ == "__main__":
    ft.app(target=App)