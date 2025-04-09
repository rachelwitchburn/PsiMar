import flet as ft

def criar_atividades(page):

    voltar = ft.Container(
                content=ft.IconButton(  
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: page.go("/patividades"),
                    icon_color="black",
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10, top=10),
            )


    return ft.View(
        route= "/",
        bgcolor="#f2dbc2",
        controls=[
            voltar
        ]
    )