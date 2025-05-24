import flet as ft
from client.src.services import PsimarAPI

def change_password(page):
    page.title = 'PsiMar'
    page.clean()
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window_maximized = True

    login = ft.TextField(
        label="Login",
        label_style=ft.TextStyle(color="black"),
        width=300,
        border_color="black",
        color="black",
        content_padding=ft.padding.symmetric(vertical=10, horizontal=10),
        bgcolor="white"
    )

    nova_senha = ft.TextField(
        label="Nova senha",
        label_style=ft.TextStyle(color="black"),
        password=True,
        can_reveal_password=True,
        width=300,
        border_color="black",
        color="black",
        content_padding=ft.padding.symmetric(vertical=10, horizontal=10),
        bgcolor="white",
    )

    repetir_nova_senha = ft.TextField(
        label="Repetir nova senha",
        label_style=ft.TextStyle(color="black"),
        password=True,
        width=300,
        border_color="black",
        color="black",
        content_padding=ft.padding.symmetric(vertical=10, horizontal=10),
        bgcolor="white",
    )


    def reset_password_request():

        if nova_senha.value != repetir_nova_senha.value:
            page.add(ft.SnackBar("As senhas não coincidem. Tente novamente."))
            return

        api = PsimarAPI()


        api.token = "seu_token_de_autenticacao_aqui"

        # Chamando a função de reset de senha
        response = api.reset_password(nova_senha.value)

        if response.status_code == 200:
            page.add(ft.SnackBar("Senha alterada com sucesso."))
        else:
            page.add(ft.SnackBar(f"Erro ao alterar a senha: {response.text}"))

    conteudo = ft.Container(
        content=ft.Column([
            login,
            nova_senha,
            repetir_nova_senha,
            ft.ElevatedButton("Confirmar", color="white", width=140, style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5),
                elevation=5,
                overlay_color="rgba(255, 255, 255, 0.2)",
                bgcolor="#212121",
                color="#white"
            ), on_click=lambda e: reset_password_request()),  # Chamando a função quando o botão for pressionado
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    return ft.View(
        route="/",
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
            conteudo,
        ]
    )
