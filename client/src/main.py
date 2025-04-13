import flet as ft

from services import PsimarAPI
from screens.login import login
from screens.psicologo_tela import psicologo
from screens.register import register
from screens.usuario_tela import usuario


def main(page: ft.Page):
    page.title = "PsiMar"
    page.window_maximized = True
    psimar_api = PsimarAPI()
    #users = psimar_api.get_users()
    #print(users)

# funcao que troca rotas pro usuario

    routes = {
        "/": login,
        "/register": register,
        "/usuario": usuario,
        "/psicologo": psicologo
    }

    def route_change(route):
        page.views.clear()
        if page.route in routes:
            page.views.append(psicologo(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")


ft.app(main, view=ft.AppView.FLET_APP)
