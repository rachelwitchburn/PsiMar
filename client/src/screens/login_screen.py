import flet as ft

from client.src.services import PsimarAPI


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
            return

        api = PsimarAPI()
        response = api.login(user_input, password_input)

        if response.status_code != 200:
            user.error_text = response.json().get("detail", "Credenciais inválidas.")
            page.update()
        else:
            data = response.json()
            token = data.get("access_token")
            user_id = data.get("user_id")
            #print("Token JWT recebido:", token)
            #print("ID do usuário:", user_id)

            # Armazena o token na sessão da página e o id
            page.session.set("token", token)
            page.session.set("user_id", user_id)

            user_type = data.get("user_type")

            if user_type == "patient":
                page.go("/user")
            elif user_type == "professional":
                page.go("/professional")
            else:
                # Fallback para caso venha um tipo desconhecido
                page.snack_bar = ft.SnackBar(ft.Text("Tipo de usuário desconhecido."))
                page.snack_bar.open = True
                page.update()

    user = ft.TextField(
        label="User",
        label_style=ft.TextStyle(color="black"),
        width=300,
        border_color="black",
        color="black",
        content_padding=ft.padding.symmetric(vertical=10, horizontal=10),
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

    content = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
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
        )
    )

    return ft.View(
        route="/",
        bgcolor="#f2dbc2",
        controls=[
            ft.Stack(
                [
                    ft.Image(
                        src="../assets/imagem.png",
                        fit=ft.ImageFit.COVER,
                        width= 1920,
                        height=1080,
                        expand=True
                    ),
                    ft.Container(
                        content=content,
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ],
                expand=True
            )
        ],
        padding=0,
        spacing=0
    )

