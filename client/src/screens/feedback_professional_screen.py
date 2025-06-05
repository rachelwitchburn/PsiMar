import flet as ft
from client.src.services import PsimarAPI


def read_feedbacks(page: ft.Page):
    token = page.session.get("token")
    professional_id = page.session.get("professional_id")

    if not token or not professional_id:
        page.go("/login")
        return  # Retorna None explicitamente para evitar problemas

    api = PsimarAPI(token=token)

    # Criação de todos os controles principais primeiro
    feedbacks_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    loading_indicator = ft.ProgressBar(visible=True)
    error_message = ft.Text("", color=ft.colors.RED)

    def load_feedbacks():
        nonlocal feedbacks_column, loading_indicator, error_message

        # Limpa os controles e mostra o loading
        feedbacks_column.controls.clear()
        loading_indicator.visible = True
        error_message.value = ""

        try:
            page.update()  # Atualiza para mostrar o loading

            response = api.get_feedback_for_professional(professional_id)

            if not response or response.status_code != 200:
                error_message.value = "Erro ao carregar feedbacks"
                return

            feedbacks = response.json()

            if not feedbacks:
                feedbacks_column.controls.append(
                    ft.Text("Nenhum feedback recebido ainda.", size=16, color="#847769")
                )
            else:
                for feedback in feedbacks:
                    message = str(feedback.get('message', 'Sem mensagem'))
                    patient_id = str(feedback.get('patient_id', 'Desconhecido'))
                    date = str(feedback.get('date', 'Data não disponível'))

                    feedback_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(message),
                                    ft.Text(f"Paciente ID: {patient_id}", size=12, color=ft.colors.GREY_600),
                                    ft.Text(f"Data: {date}", size=12, color=ft.colors.GREY_600)
                                ],
                                spacing=5
                            ),
                            padding=15
                        ),
                        margin=10
                    )
                    feedbacks_column.controls.append(feedback_card)

        except Exception as e:
            error_message.value = f"Erro: {str(e)}"
        finally:
            loading_indicator.visible = False
            try:
                page.update()
            except Exception:
                # Ignora erros de atualização se a página já foi fechada
                pass

    # Carrega os feedbacks imediatamente
    load_feedbacks()

    # Barra inferior de navegação
    app_bar = ft.BottomAppBar(
        bgcolor="#847769",
        height=55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.icons.HOUSE,
                    on_click=lambda e: page.go("/professional"),
                    icon_color=ft.colors.WHITE
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.icons.BOOK,
                    on_click=lambda e: page.go("/professional_activities"),
                    icon_color=ft.colors.WHITE
                ),
                ft.Container(expand=True),
            ]
        ),
    )

    # View principal
    view = ft.View(
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
                    loading_indicator,
                    error_message,
                    feedbacks_column
                ],
                expand=True
            )
        ]
    )

    return view