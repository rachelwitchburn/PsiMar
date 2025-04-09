import flet as ft

def mudar_senha (page):
    page.title = 'PsiMar'
    page.clean()
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window_maximized = True

    def toggle_password(e, campo):
        campo.password = not campo.password  
        campo.suffix.icon = ft.icons.VISIBILITY if campo.password else ft.icons.VISIBILITY_OFF
        page.update()    

    login = ft.TextField(
        label="Login",
        label_style=ft.TextStyle(color="black"), 
        width=300, 
        border_color="black", 
        color="black", 
        bgcolor="white"
    )

    nova_senha = ft.TextField(
        label="Nova senha",
        label_style=ft.TextStyle(color="black"),
        password=True,
        width=300,
        border_color="black",
        color="black",
        content_padding=ft.padding.symmetric(vertical=10, horizontal=10),  
        suffix=ft.IconButton(
            icon=ft.Icons.VISIBILITY, 
            icon_color="black",
            on_click= lambda e :toggle_password(e, nova_senha),
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=0)},  
                padding=ft.padding.all(0), 
            ),
        ),
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
        suffix=ft.IconButton(
            icon=ft.Icons.VISIBILITY, 
            icon_color="black",
            on_click= lambda e :toggle_password(e, repetir_nova_senha),
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=0)},  
                padding=ft.padding.all(0), 
            ),
        ),
        bgcolor="white",
    )

    conteudo = ft.Container(
    
        content= ft.Column([
            login,
            nova_senha,
            repetir_nova_senha,
            ft.ElevatedButton("Confirmar", color="white", width=140, style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5),  
                elevation=5, 
                overlay_color="rgba(255, 255, 255, 0.2)",
                bgcolor="#212121",
                color="#white")
            ),

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