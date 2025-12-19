import flet as ft
from ecotech import Auth, Database, Finance

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "EchoTech Solutions"
        self.finance = Finance()
        self.button_consulta = ft.Button(
            text="Consultar indicador",
            on_click=self.get_indicator
        )
        self.input_indicator = ft.TextField(
            hint_text="Ingresa el indicador a consultar (dolar,euro,utm,ipc,ipv,utm,uf)"
        )
        self.input_fecha = ft.TextField(
            hint_text="Ingresa fecha a consultar del indicador (Opcional)"
        )
        self.text_valor = ft.Text(
            value=""
        )
        self.build()

    def build(self):
        self.page.add(
            self.input_indicator,
            self.input_fecha,
            self.button_consulta,
            self.text_valor
        )

    def get_indicator(self,e):
        valor = self.finance.get_usd()
        print(valor)
        if valor:
            self.text_valor.value = f"{valor}"
            self.page.update()

if __name__ == "__main__":
    ft.app(target=App)
