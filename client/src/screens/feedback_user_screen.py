import flet as ft
from client.src.services.professional_api import PsimarAPI

api = PsimarAPI()

def create_feedback(page: ft.Page, patient_id: int, professional_id: int):
    feedback_field = ft.TextField(
        label="Escreva seu feedback",
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=400,
        border_radius=8,
        filled=True,
        fill_color="#ffffff",
    )

    def send_feedback(e):
        message = feedback_field.value.strip()
        if message:
            response = api.send_feedback(patient_id, professional_id, message)
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text("Feedback enviado com sucesso!"), open=True)
                feedback_field.value = ""
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao enviar feedback."), open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("O campo está vazio."), open=True)
        page.update()

    # Rodapé (igual ao modelo enviado)
    app_bar = ft.BottomAppBar(
        bgcolor="#847769",
        height=55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOUSE, on_click=lambda e: page.go("/professional"), icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.BOOK, icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
            ]
        ),
    )

    return ft.View(
        route="/feedback",
        bgcolor="#f2dbc2",
        appbar=app_bar,
        controls=[
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Deixe um feedback para seu psicólogo", size=20, color="#333333"),
                    feedback_field,
                ],
            ),
        ],
        floating_action_button=ft.FloatingActionButton(
            icon=ft.icons.SEND,
            on_click=send_feedback,
            bgcolor="#847769",
            foreground_color="white",
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )