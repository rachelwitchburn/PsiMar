import flet as ft

def login(page):
    page.title = 'PsiMar'
    page.clean()
    

    def toggle_password(e):
        Senha.password = not Senha.password  
        Senha.suffix.icon = ft.icons.VISIBILITY if Senha.password else ft.icons.VISIBILITY_OFF
        page.update()

    def login_action(e):
        if not Usuario.value:
            Usuario.error_text = "Campo obrigatório."
            page.update()
        if not Senha.value:
            Senha.error_text = "Campo obrigatório."
            page.update()
        else:
            nome = Usuario.value
            senha = Senha.value
            if nome == "1":
                page.go("/usuario")  
            elif nome == "2":
                page.go("/psicologo")
                   

    Usuario = ft.TextField(
        label="Usuário",
        width=310, 
        border_color="black", 
        color="black", 
        bgcolor="white"
    )
    
    Senha = ft.TextField(
        label="Senha",
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
                        ft.Image(src="https://svgsilh.com/png-1024/2146164.png", width=100, height=100),
                        Usuario,
                        Senha,
                        ft.ResponsiveRow(
                            
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
