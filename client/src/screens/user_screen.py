import flet as ft


def user(page):
    return ft.View(
        route="/user",
        bgcolor="#f2dbc2",
        controls=[
            ft.Container(
                alignment=ft.alignment.top_left,
                padding=10,
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: page.go("/"),
                    icon_color="black"
                )
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Área do Usuário", size=24, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text("Esta área está em construção. Em breve novas funcionalidades!"),
                    ft.Image(
                        src="assets/psi.png",  # use a imagem local se tiver
                        width=300,
                        height=300,
                        fit=ft.ImageFit.CONTAIN
                    )
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )
