import flet as ft
from datetime import datetime


def make_appointment(page):

    go_back = ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: page.go("/user"),
                    icon_color="black",
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10, top=10),
            )

    meses = [
        ft.dropdown.Option("01"),
        ft.dropdown.Option("02"),
        ft.dropdown.Option("03"),
        ft.dropdown.Option("04"),
        ft.dropdown.Option("05"),
        ft.dropdown.Option("06"),
        ft.dropdown.Option("07"),
        ft.dropdown.Option("08"),
        ft.dropdown.Option("09"),
        ft.dropdown.Option("10"),
        ft.dropdown.Option("11"),
        ft.dropdown.Option("12"),
    ]

    year_atual = datetime.now().year
    years = [ft.dropdown.Option(str(year)) for year in range(year_atual, year_atual + 16)]

    month_dropdown = ft.Dropdown(
        label="Mês",
        label_style=ft.TextStyle(color="black"),
        text_style=ft.TextStyle(color="black"),
        bgcolor= "white",
        options=meses,
        width=100)

    year_dropdown = ft.Dropdown(
        label="year",
        label_style=ft.TextStyle(color="black"),
        text_style=ft.TextStyle(color="black"),
        bgcolor="white",
        options=years,
        width=120)

    def confirm(e):
        if month_dropdown.value and year_dropdown.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Data selecionada: {month_dropdown.value}/{year_dropdown.value}")
            )
            page.snack_bar.open = True
            page.update()


    name = ft.TextField(
        label= "Nome do titular",
        label_style=ft.TextStyle(color="black"),
        hint_text="Nome do titular..",
        hint_style= ft.TextStyle(color= "#767676"),
        border_color= "black",
        bgcolor= "white"
    )

    card_number = ft.TextField(
        label= "Número do cartão",
        label_style=ft.TextStyle(color="black"),
        hint_text= "Número do cartão...",
        hint_style= ft.TextStyle(color= "#767676"),
        border_color= "black",
        bgcolor= "white"
    )


    password = ft.TextField(
        label= "Senha do cartão",
        label_style= ft.TextStyle(color= "black"),
        hint_text= "Senha",
        hint_style= ft.TextStyle(color= "#767676"),
        password= True,
        can_reveal_password= True,
        bgcolor= "white",
        border_color= "black"
    )

    conteudo= ft.Container(
        content= ft.Column(
            controls= [
                name,
                card_number,
                password,
                month_dropdown,
                year_dropdown
            ],
            alignment=  ft.MainAxisAlignment.CENTER,
        )
    )



    return ft.View(
        route="/user",
        bgcolor="#f2dbc2",

        controls=[
            go_back,
            conteudo

        ],

    )