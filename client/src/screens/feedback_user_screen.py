import flet as ft
from client.src.services.professional_api import PsimarAPI

def create_feedback(page: ft.Page):
    token = page.session.get("token")
    patient_id = page.session.get("user_id")

    if not token or not patient_id:
        page.go("/")
        return

    api = PsimarAPI(token=token)
    professional_id = 2  # Isso deve vir da sessão ou de outra forma dinâmica

    feedback_field = ft.TextField(
        label="Escreva seu feedback",
        label_style=ft.TextStyle(color="black"),
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=400,
        border_radius=8,
        filled=True,
        fill_color="#ffffff",
        text_style=ft.TextStyle(color="#847769")
    )

    page.snack_bar = ft.SnackBar(content=ft.Text(""))


    def send_feedback(e):
        message = feedback_field.value.strip()
        if message:
            response = api.send_feedback(
                patient_id=patient_id,
                professional_id=professional_id,
                message=message
            )
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Feedback enviado com sucesso!"),
                    bgcolor=ft.colors.GREEN_400
                )
                feedback_field.value = ""
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Erro ao enviar feedback: {response.text}"),
                    bgcolor=ft.colors.RED_400
                )
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, escreva seu feedback antes de enviar"),
                bgcolor=ft.colors.ORANGE_400
            )

        page.snack_bar.open = True
        page.update()

    app_bar = ft.BottomAppBar(
        bgcolor="#847769",
        height=55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.icons.HOUSE,
                    on_click=lambda e: page.go("/user"),
                    icon_color=ft.colors.WHITE
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.icons.BOOK,
                    on_click=lambda e: page.go("/patient_activities"),
                    icon_color=ft.colors.WHITE
                ),
                ft.Container(expand=True),
            ]
        ),
    )

    return ft.View(
        route="/feedback",
        bgcolor="#f2dbc2",
        appbar=app_bar,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Deixe seu feedback", size=20, weight=ft.FontWeight.BOLD, color="#847769"),
                        feedback_field,
                    ],
                ),
            )
        ],
        floating_action_button=ft.FloatingActionButton(
            icon=ft.icons.SEND,
            on_click=send_feedback,
            bgcolor="#847769",
            foreground_color="white",
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )
