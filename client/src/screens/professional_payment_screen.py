import flet as ft
from datetime import datetime
from client.src.services import PsimarAPI


def payments_view(page: ft.Page):
    page.title = "Pagamentos Recebidos"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#f2dbc2"
    page.padding = 20

    # Verifica autenticação
    token = page.session.get("token")
    if not token:
        page.go("/")
        return

    api = PsimarAPI(token=token)
    professional_id = page.session.get("user_id")

    # Elementos da interface
    loading_indicator = ft.ProgressRing(visible=True)
    error_message = ft.Text(visible=False, color=ft.colors.RED)
    payments_list = ft.ListView(expand=True, spacing=10)

    def format_date(date_str):
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M")
        except:
            return date_str

    def create_payment_card(payment):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PAYMENT, color="#847769"),
                            title=ft.Text(f"R$ {payment['amount']:.2f}", weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Paciente: {payment['patient_name']}"),
                        ),
                        ft.Row(
                            [
                                ft.Text(f"Data: {format_date(payment['created_at'])}"),
                                ft.Container(width=20),
                                ft.Chip(
                                    label=ft.Text(payment['status'].capitalize()),
                                    bgcolor=ft.colors.GREEN_100 if payment['status'] == "paid" else ft.colors.ORANGE_100
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ],
                    spacing=0
                ),
                padding=10,
            )
        )

    def load_payments():
        try:
            loading_indicator.visible = True
            error_message.visible = False
            payments_list.controls.clear()
            page.update()

            response = api.get_payments()

            if response.status_code == 200:
                all_payments = response.json()
                # Filtra apenas os pagamentos deste profissional
                professional_payments = [
                    p for p in all_payments
                    if p.get('professional_id') == professional_id
                ]

                if not professional_payments:
                    payments_list.controls.append(
                        ft.Text("Nenhum pagamento recebido ainda", style=ft.TextStyle(italic=True))
                    )
                else:
                    for payment in professional_payments:
                        payments_list.controls.append(create_payment_card(payment))
            else:
                error_message.value = f"Erro ao carregar pagamentos: {response.text}"
                error_message.visible = True

        except Exception as e:
            error_message.value = f"Erro: {str(e)}"
            error_message.visible = True
        finally:
            loading_indicator.visible = False
            page.update()

    # Carrega os pagamentos ao abrir a tela
    load_payments()

    # Layout da página
    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Pagamentos Recebidos", size=24, weight=ft.FontWeight.BOLD, color="#847769"),
                    ft.IconButton(
                        icon=ft.icons.REFRESH,
                        on_click=lambda e: load_payments(),
                        tooltip="Recarregar"
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(height=20),
            loading_indicator,
            error_message,
            payments_list
        ],
        spacing=10,
        expand=True
    )

    # Barra inferior de navegação
    app_bar = ft.BottomAppBar(
        bgcolor="#847769",
        height=55,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOME, on_click=lambda e: page.go("/professional"),
                              icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.PAYMENT, icon_color=ft.colors.WHITE, selected=True),
                ft.Container(expand=True),
            ]
        ),
    )

    return ft.View(
        route="/professional/payments",
        bgcolor="#f2dbc2",
        appbar=app_bar,
        controls=[content],
    )