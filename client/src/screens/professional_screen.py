import flet as ft

def psychologist(page):
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
    page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD)
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    popupmenu = ft.Container(
        content=ft.PopupMenuButton(
            icon=ft.icons.MENU,
            icon_color= "#847769",
            bgcolor= "white",
            items=[
                ft.PopupMenuItem(
                    content= ft.Row([
                        ft.Icon(ft.icons.ADD, color= "#847769"),
                        ft.Text("Gerenciar Horários", color="#847769"),
                    ]),
                    on_click=lambda e: page.go("/agenda"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.icons.LOGOUT, color= "#847769"),
                        ft.Text("Sair", color= "#847769"),
                    ]),
                    on_click=lambda e: page.go("/"),
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


    appBar =  ft.BottomAppBar(
        bgcolor="#847769",
        height= 55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOUSE, icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.BOOK, on_click= lambda e: page.go("/professional_activities"),icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
            ]
        ),
    )
    #logout = ft.Container(
    #            content=ft.IconButton(
    #                icon=ft.icons.LOGOUT,
    #                on_click=lambda e: page.go("/"),
    #                icon_color="black",
    #            ),
    #            alignment=ft.alignment.top_right,
    #            padding=ft.padding.only(left=10, top=10),
    #        )



    return ft.View(
        route="/",
        bgcolor="#f2dbc2",
        appbar=appBar,
        controls=[
            popupmenu,
            #logout,
            agendamentos,
        ],

)