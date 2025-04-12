import flet as ft

from services import PsimarAPI
from screens.login import login
from screens.psicologo_tela import psicologo
from screens.register import register
from screens.usuario_tela import usuario


def main(page: ft.Page):
    page.title = "PsiMar"
    psimar_api = PsimarAPI()
    users = psimar_api.get_users()
    print(users)

"""
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(login(page))
        elif page.route == "/register":
            page.views.append(register(page))
        elif page.route == "/usuario":
            page.views.append(usuario(page))
        elif page.route == "/psicologo":
            page.views.append(psicologo(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")

"""
ft.app(main, view=ft.AppView.FLET_APP)
