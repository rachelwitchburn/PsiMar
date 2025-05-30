import flet as ft

from src.services import PsimarAPI


def login(page):
    page.title = 'PsiMar'
    page.clean()
    


    def toggle_password():
        Passwords.password = not Passwords.password
        Passwords.suffix.icon = ft.icons.VISIBILITY if Passwords.password else ft.icons.VISIBILITY_OFF
        page.update()

    def login_action(e):
        user_input = User.value
        password_input = Passwords.value

        User.error_text = ""
        Passwords.error_text = ""
        if not user_input:
            User.error_text = "Campo obrigatório."
        if not password_input:
            Passwords.error_text = "Campo obrigatório."
        page.update()

        if User.error_text or Passwords.error_text:
            return  # para execução se tiver erro

        # Caso 1: Psicólogo - login com código de acesso
        if user_input.startswith("PSI"):  # supondo que códigos comecem com 'PSI'
            response = PsimarAPI().login_professional(user_input)

            if "error" in response:
                User.error_text = response["error"]
                page.update()
            else:
                page.go("/psicologo")

        # Caso 2: Paciente - login com e-mail/nome + senha
        else:
            response = PsimarAPI().login_patient(user_input, password_input)

            if "error" in response:
                User.error_text = response["error"]
                page.update()
            else:
                page.go("/usuario")

    User = ft.TextField(
        label="Usuário",
        width=310, 
        border_color="black", 
        color="black", 
        bgcolor="white"
    )

    Passwords = ft.TextField(
        label="Passwords",
        label_style=ft.TextStyle(color="black"),
        password=True,
        width=310,
        border_color="black",
        color="black",
        content_padding=ft.padding.symmetric(vertical=10, horizontal=10),  
        suffix=ft.IconButton(
            icon=ft.Icons.VISIBILITY, 
            icon_color="black",
            on_click=toggle_password
        ),
        bgcolor="white",   
    )

    conteudo = ft.Stack(
        expand=True,
        alignment=ft.alignment.center,
        controls=[
            ft.Image(src="imagem.png", fit=ft.ImageFit.COVER, expand=True),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [
                        ft.Image(src="../assets/psi.png", width=100, height=100),
                        User,
                        Passwords,
                        ft.Row(
                            [
                                ft.Container(
                                    col ={"xs":1}
                                ),

                                ft.Column(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Login", 
                                            on_click=login_action, 
                                            color="white", 
                                            width=175, 
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=5),  
                                                elevation=5, 
                                                bgcolor="#847769",
                                                color="white"
                                            )
                                        )
                                    ],
                                    col={"xs": 5, "md": 5},  
                                   
                                ),
                                ft.Column(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Registrar", 
                                            on_click=lambda e: page.go("/register"), 
                                            width=175, 
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=5),  
                                                elevation=5, 
                                                bgcolor="#847769",
                                                color="white"
                                            )
                                        )
                                    ],
                                    col={"xs": 5, "md": 5},  
                                    
                                ),
                            ], 
                            
                        ),
                        ft.TextButton(
                            "Esqueci minha senha", 
                            on_click=lambda e: page.go("/nsenha"),
                            style=ft.ButtonStyle(color="#847769")
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                expand=True
            )
        ]
    )

    return ft.View(
        route="/",
        bgcolor="#f2dbc2",
        controls=[conteudo]
    )
