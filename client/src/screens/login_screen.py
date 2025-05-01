import flet as ft

from src.services import PsimarAPI


def login(page):
    page.title = 'PsiMar'
    page.clean()
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window_maximized = True



    def login_action(e):
        user_input = user.value
        password_input = passwords.value

        user.error_text = ""
        passwords.error_text = ""
        if not user_input:
            user.error_text = "Campo obrigatório."
        if not password_input:
            passwords.error_text = "Campo obrigatório."
        page.update()

        if user.error_text or passwords.error_text:
            return  # para execução se tiver erro

        api = PsimarAPI()
        response = api.login(user_input, password_input)

        # Caso 1: Psicólogo - login com código de acesso
        if response.status_code != 200:
            user.error_text = response.json().get("detail", "Credenciais inválidas.")
            page.update()
        else:
            page.go("/user")

        # Caso 2: Paciente - login com e-mail/nome + senha



    user = ft.TextField(
        label="User",
        label_style=ft.TextStyle(color="black"),
        width=300,
        border_color="black",
        color="black",
        bgcolor="white"
    )

    passwords = ft.TextField(
        label="Password",
        label_style=ft.TextStyle(color="black"),
        password=True,
        can_reveal_password=True,
        width=300,
        border_color="black",
        color="black",
        content_padding=ft.padding.symmetric(vertical=10, horizontal=10),
        bgcolor="white",
    )

    content = ft.Stack(
        alignment=ft.alignment.center,
        controls=[
            ft.Image(src="../assets/imagem.png", fit=ft.ImageFit.COVER, expand=True),

            ft.Container(
                content=ft.Column(
                    [
                        ft.Image(src="../assets/psi.png", width=100, height=100),
                        user,
                        passwords,
                        ft.Row(
                            [
                                ft.ElevatedButton("Login", on_click=login_action, color="white", width=140,
                                                  style=ft.ButtonStyle(
                                                      shape=ft.RoundedRectangleBorder(radius=5),
                                                      elevation=5,
                                                      overlay_color="rgba(255, 255, 255, 0.2)",
                                                      bgcolor="#212121",
                                                      color="#white")
                                                  ),
                                ft.ElevatedButton("Registrar", on_click=lambda e: page.go("/register"), width=140,
                                                  style=ft.ButtonStyle(
                                                      shape=ft.RoundedRectangleBorder(radius=5),
                                                      elevation=5,
                                                      overlay_color="rgba(255, 255, 255, 0.2)",
                                                      bgcolor="#212121",
                                                      color="white")
                                                  )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        ),
                        ft.TextButton(
                            "Esqueci minha senha",
                            on_click=lambda e: page.go("/changePass"),
                            style=ft.ButtonStyle(color="#847769")
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ],
    )

    return ft.View(
        route="/",
        bgcolor="#f2dbc2",
        controls=[
            content
        ]
    )
