import flet as ft
from flet_core import FontWeight


def register(page):
    page.title = 'PsiMar'

    password = ft.Ref[ft.TextField]()
    confirm_password = ft.Ref[ft.TextField]()
    username = ft.Ref[ft.TextField]()



    def show_form(user_type):
        form_container.clean()
        form_container.content = create_form(user_type)
        page.update()

    def handle_register(user_type: str):
        if not username.current.value or not password.current.value or not confirm_password.current.value:
            show_message("Todos os campos são obrigatórios.")
            return

        if password.current.value != confirm_password.current.value:
            show_message("As senhas não coincidem.")
            return

        # Aqui você pode fazer a requisição à API futuramente
        destination = "/professional" #if user_type == "/professional" else "/user"
        page.go(destination)

    def show_message(msg: str):
        page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor="red")
        page.snack_bar.open = True
        page.update()

    def create_form(user_type: str):
        return ft.Column([
            ft.TextField(
                ref=username,
                label="Código" if user_type == "professional" else "Email",
                label_style=ft.TextStyle(color="black"),
                width=300,
                border_color="black",
                color="black",
                bgcolor="white"
            ),
            ft.TextField(
                ref=password,
                label="Senha",
                label_style=ft.TextStyle(color="black"),
                password=True,
                can_reveal_password=True,
                width=300,
                border_color="black",
                color="black",
                bgcolor="white",
            ),
            ft.TextField(
                ref=confirm_password,
                label="Confirmar Senha",
                label_style=ft.TextStyle(color="black"),
                password=True,
                can_reveal_password=True,
                width=300,
                border_color="black",
                color="black",
                bgcolor="white",
            ),
            ft.ElevatedButton(
                "Registrar",
                on_click=lambda e: handle_register(user_type),
                width=150,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5),
                    elevation=5,
                    overlay_color="rgba(255, 255, 255, 0.2)",
                    bgcolor="black",
                    color="white"
                )
            )
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    form_container = ft.Container()

    return ft.View(
        route="/register",
        bgcolor="#f2dbc2",
        controls=[
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: page.go("/"),
                    icon_color="black",
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10, top=10),
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Escolha seu perfil:", size=20, weight=FontWeight.BOLD, color="black"),
                    ft.Row([
                        ft.ElevatedButton("Sou Psicólogo", on_click=lambda e: show_form("psicologo"),
                                          style=ft.ButtonStyle(
                                              shape=ft.RoundedRectangleBorder(radius=5),
                                              elevation=5,
                                              overlay_color="rgba(255, 255, 255, 0.2)",
                                              bgcolor="black",
                                              color="white"
                                          )),
                        ft.ElevatedButton("Sou Paciente", on_click=lambda e: show_form("paciente"),
                                          style=ft.ButtonStyle(
                                              shape=ft.RoundedRectangleBorder(radius=5),
                                              elevation=5,
                                              overlay_color="rgba(255, 255, 255, 0.2)",
                                              bgcolor="black",
                                              color="white"
                                          )),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    form_container,
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                expand=True
            )
        ]
    )
