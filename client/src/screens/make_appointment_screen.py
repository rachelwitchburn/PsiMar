import flet as ft


def make_appointment(page):

    go_back = ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: page.go("/user"),
                    icon_color="black",
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10, top=10),
            )


    return ft.View(
        route="/user",
        bgcolor="#f2dbc2",

        controls=[
            go_back,
            ft.Text("nada ainda", color="black")

        ],

    )