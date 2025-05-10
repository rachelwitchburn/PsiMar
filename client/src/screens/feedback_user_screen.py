import flet as ft
from flet_core import FontWeight


def create_feedback(page):

    feedback = ft.Container(
        content=
        ft.TextField(
            border_color="black",
            color="black",
            bgcolor="white",
            hint_text="Deixe seu feedback",
            hint_style=ft.TextStyle(color="#767676"),
            multiline=True,
            min_lines=4,
            max_lines=20,
            expand=True,
        ),
        padding=20,
        width=1600,


    )


    return ft.View(
        route="/user",
        bgcolor="#f2dbc2",
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Nos dê o seu feedback", size=20, weight=FontWeight.BOLD, color="black"),
                    feedback,
                    ft.ElevatedButton("Publicar",
                                      style=ft.ButtonStyle(
                                          shape=ft.RoundedRectangleBorder(radius=5),
                                          elevation=5,
                                          overlay_color="rgba(255, 255, 255, 0.2)",
                                          bgcolor="black",
                                          color="white"
                                      )),

                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        ],
    )
