import flet as ft
from flet_core import FontWeight
from src.services import PsimarAPI


def create_activities(page):

    title = ft.TextField(
        border_color="black",
        color="black",
        bgcolor="white",
        hint_text="Título",
        hint_style=ft.TextStyle(color="#767676")
    )

    description = ft.TextField(
        border_color="black",
        color="black",
        bgcolor="white",
        hint_text="Descrição",
        hint_style=ft.TextStyle(color="#767676")
    )

    # Mostra quem foi selecionado
    selected_patient = ft.Text(value="", color="black")

    # Dropdown vazio, vamos preencher depois
    dropdown = ft.Dropdown(
        label="Selecione um paciente",
        hint_text="Clique no botão para carregar",
        options=[],
        on_change=lambda e: (
            setattr(selected_patient, "value", f"Paciente selecionado: {e.control.value}"),
            page.update()
        )
    )

    # Botão que faz a requisição e preenche o dropdown
    def carregar_pacientes(e):
        api = PsimarAPI()
        response = api.get_patients()
        if response.status_code == 200:
            patients = response.json()
            dropdown.options = [
                ft.dropdown.Option(
                    f"{p['first_name']} {p['last_name']} ({p['email']})"
                ) for p in patients
            ]
            page.update()

    btn_carregar = ft.ElevatedButton("Escolher paciente", on_click=carregar_pacientes)

    go_back = ft.Container(
        content=ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda e: page.go("/professional_activities"),
            icon_color="black",
        ),
        alignment=ft.alignment.top_left,
        padding=ft.padding.only(left=10, top=10),
    )

    content = ft.Container(
        content=ft.Column(
            controls=[
                go_back,
                ft.Text("Criar uma atividade:", size=20, weight=FontWeight.BOLD, color="black"),
                title,
                description,

                # Botão para carregar pacientes + Dropdown + Texto de retorno
                btn_carregar,
                dropdown,
                selected_patient,

                ft.ElevatedButton(
                    "Criar Atividade",
                    width=140,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5),
                        elevation=5,
                        overlay_color="rgba(255, 255, 255, 0.2)",
                        bgcolor="#212121",
                        color="white"
                    )
                )
            ],
        ),
    )

    return ft.View(
        route="/",
        bgcolor="#f2dbc2",
        controls=[content]
    )
