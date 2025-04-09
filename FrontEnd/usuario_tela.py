import flet as ft

def usuario(page):
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


    appBar =  ft.BottomAppBar(
        bgcolor="#847769",
        height= 55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.HOUSE, icon_color=ft.Colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.BOOK, on_click= lambda e: page.go("/uatividades"),icon_color=ft.Colors.WHITE),
                ft.Container(expand=True),
            ]
        ),
    )

    logout = ft.Container(
                content=ft.IconButton(  
                    icon=ft.icons.LOGOUT,
                    on_click=lambda e: page.go("/"),
                    icon_color="black",
                ),
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(left=10, top=10),
            )



    return ft.View(
        route="/usuario",
        bgcolor="#f2dbc2",
        appbar=appBar,
        controls=[
            logout,
            agendamentos,
        ],
        floating_action_button=ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=lambda e: page.go("/agendar"),
            bgcolor= "#847769",
            foreground_color= "white",
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
)
