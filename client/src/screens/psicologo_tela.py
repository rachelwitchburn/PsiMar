import flet as ft

def psicologo(page):
    page.title = 'PsiMar'
    page.clean()

    agendamentos = ft.Column(
        expand=True, 
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text("As consultas marcadas ficam aqui!", color="black")
            ),
        ],
    )

    page.floating_action_button = ft.FloatingActionButton(icon=ft.Icons.ADD)
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    appBar = ft.BottomAppBar(
        bgcolor="#847769",
        height=55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.HOUSE, icon_color=ft.Colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.BOOK, on_click=lambda e: page.go("/patividades"), icon_color=ft.Colors.WHITE),
                ft.Container(expand=True),
            ]
        ),
    )


    popupmenu = ft.Container(
        content=ft.PopupMenuButton(
            icon=ft.icons.MENU,
            icon_color= "#847769",
            bgcolor= "white",
            items=[
                ft.PopupMenuItem(
                    content= ft.Row([
                        ft.Icon(ft.Icons.ADD, color= "#847769"),
                        ft.Text("Gerenciar Horários", color="#847769"),
                    ]),
                    on_click=lambda e: page.go("/ghorarios"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LOGOUT, color= "#847769"),
                        ft.Text("Sair", color= "#847769"),
                    ]),
                    on_click=lambda e: page.go("/"),
                )
            ]
        ),
        alignment=ft.alignment.top_right,
        padding=ft.padding.only(left=10, top=10),
    )

    return ft.View(
        route="/usuario",
        bgcolor="#f2dbc2",
        appbar=appBar,
        controls=[
            popupmenu,
            agendamentos,
        ],
    )
