import flet as ft
import os
from ecotech import Auth, Database, Finance
from dotenv import load_dotenv
load_dotenv()


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "EchoTech Solutions"
        self.db = Database(
            username=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=os.getenv("ORACLE_DSN")
        )
        self.finance = Finance()

        # Crear tablas
        self.db.create_all_tables()
        # Empieza la aplicación en menu_register
        self.menu_register()

    # Menu de Registro
    def menu_register(self):
        self.page.controls.clear()
        self.input_username = ft.TextField(
            hint_text="Ingresa un nombre de usuario"
        )
        self.input_password = ft.TextField(
            hint_text="Ingresa tu contraseña",
            can_reveal_password=True,
            password=True
        )
        self.button_register = ft.Button(
            text="Registrarse",
            on_click=self.handle_register
        )
        self.text_status = ft.Text(
            value=""
        )
        self.page.add(
            self.input_username,
            self.input_password,
            self.button_register,
            self.text_status
        )
        self.page.update()

    def handle_register(self, e):
        username = (self.input_username.value or "").strip()
        password = (self.input_password.value or "").strip()
        if Auth.register(self.db, 1, username, password):
            self.text_status.value = "Registrado exitosamente"
        else:
            self.text_status.value = "No se pudo registrar"
        self.page.update()

    # Menu Login
    # Menu Principal


if __name__ == "__main__":
    ft.app(target=App)
