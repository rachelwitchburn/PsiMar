import flet as ft

def usuario(page):
    return ft.View(
        route="/usuario",
        bgcolor="#f2dbc2",
        controls=[
            ft.Container(
                content=ft.Image(
                    src="https://static.vecteezy.com/ti/vetor-gratis/p1/1218694-sinal-de-aviso-em-construcao-gratis-vetor.jpg"
                ),
                alignment=ft.alignment.center, 
                expand=True  
            )
        ]
    )
