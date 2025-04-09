import flet as ft

def patividades (page):



    appBar =  ft.BottomAppBar(
        bgcolor="#847769",
        height= 55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.HOUSE,on_click= lambda e: page.go("/psicologo"), icon_color=ft.Colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.BOOK,icon_color=ft.Colors.WHITE),
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
            icon=ft.Icons.ADD,
            on_click=lambda e: page.go("/criaratividades"),
            bgcolor= "#847769",
            foreground_color= "white",
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )