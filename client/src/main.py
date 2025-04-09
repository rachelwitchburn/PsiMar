import flet as ft

from screens.login import login
from screens.register import register
from screens.usuario_tela import usuario
from screens.psicologo_tela import psicologo
from screens.mudar_senha import mudar_senha
from screens.usuario_atividades import uatividades
from screens.psicologo_atividades import patividades
from screens.agendar_consulta import agendar_consulta
from screens.criar_atividades import criar_atividades
from screens.gerenciar_horarios import gerenciar_horarios


def main(page: ft.Page):
    page.window.width = 380  
    page.window.height = 700  
    page.window.resizable = False
    page.update()


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
        elif page.route == "/nsenha":
            page.views.append(mudar_senha(page)) 
        elif page.route == "/uatividades":
            page.views.append(uatividades(page))
        elif page.route == "/patividades":
            page.views.append(patividades(page))            
        elif page.route == "/agendar":
            page.views.append(agendar_consulta(page))
        elif page.route == "/criaratividades":
            page.views.append(criar_atividades(page))
        elif page.route == "/ghorarios":
            page.views.append(gerenciar_horarios(page))                    
        page.update()

    page.on_route_change = route_change
    page.go("/")


ft.app(main, view=ft.AppView.FLET_APP)
