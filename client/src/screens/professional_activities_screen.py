import flet as ft

def professional_activities (page):



    appBar =  ft.BottomAppBar(
        bgcolor="#847769",
        height= 55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOUSE,on_click= lambda e: page.go("/professional"), icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.BOOK,icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
            ]
        ),
    )

    return ft.View(
        route="/",
        bgcolor="#f2dbc2",
        appbar= appBar,
        controls=[
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text("precisa ter atividades aqui", color="black")
                    ),
                ],
            )
            ],
        floating_action_button=ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=lambda e: page.go("/create_activities"),
            bgcolor= "#847769",
            foreground_color= "white",
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )