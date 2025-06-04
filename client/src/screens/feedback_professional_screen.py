import flet as ft
from client.src.services import PsimarAPI


def read_feedbacks(page: ft.Page):
    token = page.session.get("token")
    professional_id = page.session.get("professional_id")

    if not token or not professional_id:
        page.go("/login")
        return

    api = PsimarAPI(token=token)
    feedbacks_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def load_feedbacks():
        feedbacks_column.controls.clear()

        try:
            response = api.get_feedback_for_professional(professional_id)

            if response.status_code == 200:
                feedbacks = response.json()

                if not feedbacks:
                    feedbacks_column.controls.append(
                        ft.Text("Nenhum feedback recebido ainda.", size=16, color="#847769")
                    )
                else:
                    for feedback in feedbacks:

                        feedbacks_column.controls.append(
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column(
                                        controls=[  # Adicionado lista explícita de controles
                                            ft.Text(feedback.get('message', '')),
                                            ft.Text(
                                                f"Paciente ID: {feedback.get('patient_id', '')}",
                                                size=12,
                                                color=ft.colors.GREY_600
                                            ),
                                            ft.Text(
                                                f"Data: {feedback.get('date', '')}",
                                                size=12,
                                                color=ft.colors.GREY_600
                                            )
                                        ],
                                        spacing=5
                                    ),
                                    padding=15
                                ),
                                margin=10
                            )
                        )
            else:
                feedbacks_column.controls.append(
                    ft.Text(f"Erro ao carregar feedbacks: {response.text}", color=ft.colors.RED)
                )

        except Exception as e:
            feedbacks_column.controls.append(
                ft.Text(f"Erro: {str(e)}", color=ft.colors.RED)
            )

        page.update()

    load_feedbacks()

    app_bar = ft.BottomAppBar(
        bgcolor="#847769",
        height=55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOUSE, on_click=lambda e: page.go("/professional"),
                              icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.BOOK, on_click=lambda e: page.go("/professional_activities"),icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
            ]
        ),
    )

    return ft.View(
        route="/feedback_professional",
        bgcolor="#f2dbc2",
        appbar=app_bar,
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("Feedbacks Recebidos", size=20, weight=ft.FontWeight.BOLD, color="#847769"),

                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=10)
                    ),
                    ft.Divider(height=1),
                    feedbacks_column
                ],
                expand=True
            )
        ]
    )