import flet as ft
from client.src.services import PsimarAPI

def psychologist(page):
    page.title = 'PsiMar'
    page.clean()

    token = page.session.get("token")

    if not token:
        print(" Nenhum token encontrado na sessão! Redirecionando para login...")
        page.go("/")
        return

    api = PsimarAPI(token=token)
    response = api.get_patients()

    lista_widgets = []

    if response.status_code == 200:
        pacientes = response.json()

        if not pacientes:
            lista_widgets.append(
                ft.Text("Nenhum paciente encontrado.", color="black")
            )
        else:
            for paciente in pacientes:
                nome = f"{paciente.get('first_name', '')} {paciente.get('last_name', '')}"
                email = paciente.get('email', 'Sem email')

                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Nome: {nome}", color="black"),
                            ft.Text(f"E-mail: {email}", color="black"),
                        ]),
                        padding=10,
                        bgcolor="#f5f5f5",
                        border_radius=10,
                    )
                )
                lista_widgets.append(card)
    else:
        lista_widgets.append(
            ft.Text("Erro ao buscar pacientes. Verifique a conexão ou permissões.", color="red")
        )

    def logout(page):
        page.session.remove("token")
        print("token removido, fechando sessão")
        page.go("/")

    agendamentos = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=lista_widgets
    )

    page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD)
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    popupmenu = ft.Container(
        content=ft.PopupMenuButton(
            icon=ft.icons.MENU,
            icon_color="#847769",
            bgcolor="white",
            items=[
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.icons.ADD, color="#847769"),
                        ft.Text("Gerenciar Horários", color="#847769"),
                    ]),
                    on_click=lambda e: page.go("/agenda"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.icons.LOGOUT, color="#847769"),
                        ft.Text("Sair", color="#847769"),

                    ]),
                    on_click=lambda e: logout(page),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.icons.FEEDBACK, color="#847769"),
                        ft.Text("Ver feedback", color="#847769"),
                    ]),
                    on_click=lambda e: page.go("/feedback_professional"),
                ),
            ]
        ),
        alignment=ft.alignment.top_right,
        padding=ft.padding.only(left=10, top=10),
    )

    appBar = ft.BottomAppBar(
        bgcolor="#847769",
        height=55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOUSE, icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.icons.BOOK,
                    on_click=lambda e: page.go("/professional_activities"),
                    icon_color=ft.colors.WHITE
                ),
                ft.Container(expand=True),
            ]
        ),
    )

    return ft.View(
        route="/",
        bgcolor="#f2dbc2",
        appbar=appBar,
        controls=[
            popupmenu,
            agendamentos,
        ],
    )
