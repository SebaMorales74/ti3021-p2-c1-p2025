"""
Saludar al usuario al ingresar su nombre
"""
import flet as ft


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hola 🐍"

        self.input_nombre = ft.TextField(
            label="Nombre",
            hint_text="Ingresa tu nombre"
        )
        self.button_saludar = ft.Button(
            text="Saludar",
            on_click=self.on_saludar
        )
        self.text_saludar = ft.Text(
            value=""
        )

        self.build()

    def build(self):
        self.page.add(
            self.input_nombre,
            self.button_saludar,
            self.text_saludar
        )

    def on_saludar(self, e):
        nombre = (self.input_nombre.value or "").strip()

        if not nombre:
            self.text_saludar.value = "Ingresa un nombre."
        else:
            self.text_saludar.value = f"Hola {nombre}"
        self.page.update()


if __name__ == "__main__":
    ft.app(target=App)
