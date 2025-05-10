import flet as ft

from services import PsimarAPI
from screens.login_screen import login
from screens.professional_screen import psychologist
from screens.register_screen import register
from screens.user_screen import user


def main(page: ft.Page):
    page.title = "PsiMar"
    page.window_maximized = True

    page.client = PsimarAPI()


# funcao que troca rotas pro usuario

    routes = {
        "/": login,
        "/register": register,
        "/user": user,
        "/professional": psychologist
    }

    def route_change(route):
        page.views.clear()
        view_fn = routes.get(page.route, lambda p: ft.View(route, [ft.Text("Página não encontrada")]))
        page.views.append(view_fn(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")


ft.app(main, view=ft.AppView.FLET_APP)
