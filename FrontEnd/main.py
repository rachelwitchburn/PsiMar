import flet as ft
from login import login
from register import register
from usuario_tela import usuario
from psicologo_tela import psicologo

def main(page: ft.Page):

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

ft.app(main , view= ft.AppView.FLET_APP)  
