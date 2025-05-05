import flet as ft

def agenda(page):

    a = ft.Container(
        content= ft.Text("ui ui ui", color="black")
    )


    return ft.View(
        route="/",
        bgcolor="#f2dbc2",

        controls=[
            a
        ],

    )