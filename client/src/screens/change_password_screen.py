import flet as ft
from client.src.services import PsimarAPI


def change_password(page):
    page.title = 'PsiMar - Alterar Senha'
    page.clean()
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window_maximized = True

    token = page.session.get("token")
    if not token:
        print("Nenhum token encontrado na sessão! Redirecionando para login...")
        page.go("/")
        return

    api = PsimarAPI(token=token)
    user_type = page.session.get("user_type")

    nova_senha = ft.TextField(
        label="Nova senha (mínimo 6 caracteres)",
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
        can_reveal_password=True,
        width=300,
        border_color="black",
        color="black",
        content_padding=ft.padding.symmetric(vertical=10, horizontal=10),
        bgcolor="white",
    )

    def show_snackbar(message, color="red"):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=color,
            behavior=ft.SnackBarBehavior.FLOATING,
        )
        page.snack_bar.open = True
        page.update()

    def reset_password_request(e):
        if not nova_senha.value or not repetir_nova_senha.value:
            show_snackbar("Por favor, preencha ambos os campos")
            return

        if len(nova_senha.value) < 6:
            show_snackbar("A senha deve ter pelo menos 6 caracteres")
            return

        if nova_senha.value != repetir_nova_senha.value:
            show_snackbar("As senhas não coincidem")
            return

        try:
            response = api.reset_password({"nova_senha": nova_senha.value})
            if response.status_code == 200:
                show_snackbar("Senha alterada com sucesso!", "green")
                if user_type == 'patient':
                    page.go("/patient")
                else:# Redireciona após sucesso
                    page.go("/professional")
            else:
                show_snackbar(f"Erro ao alterar senha: {response.text}")
        except Exception as e:
            show_snackbar(f"Erro de conexão: {str(e)}")

    conteudo = ft.Container(
        content=ft.Column([
            ft.Text("Alterar Senha", size=24, weight="bold", color="black"),
            nova_senha,
            repetir_nova_senha,
            ft.ElevatedButton(
                "Confirmar",
                width=300,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5),
                    bgcolor="#212121",
                    color="white"
                ),
                on_click=reset_password_request
            ),
        ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    return ft.View(
        route="/change_password",
        bgcolor="#f2dbc2",
        controls=[
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: page.go("/patient") if user_type == 'patient' else lambda  e: page.go("/professioanl"),
                    icon_color="black",
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10, top=10),
            ),
            conteudo,
        ]
    )