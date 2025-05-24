import flet as ft

from api.app.main import professional_home
from client.src.services import PsimarAPI

def payment(page: ft.Page):
    page.title = "Realizar Pagamento"
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
    patient_id = page.session.get("user_id")
    professional_id = 2

    # Elementos do formulário
    amount_field = ft.TextField(
        label="Valor",
        prefix_text="R$ ",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color="#847769",
        width=300,
        text_size=16,
        bgcolor= "white"
    )


    payment_method = ft.Dropdown(
        label="Método de Pagamento",
        options=[
            ft.dropdown.Option("Pix"),
            ft.dropdown.Option("Cartão de Crédito"),
            ft.dropdown.Option("Boleto Bancário"),
        ],
        border_color="#847769",
        width=300,



    )

    submit_button = ft.ElevatedButton(
        "Realizar Pagamento",
        icon=ft.icons.PAYMENT,
        bgcolor="#847769",
        color="white",
        width=300,
        height=50
    )

    loading_indicator = ft.ProgressRing(visible=False)
    status_message = ft.Text(visible=False)

    def process_payment(e):
        # Validação dos campos
        if not amount_field.value or not payment_method.value:
            show_status("Preencha todos os campos obrigatórios", is_error=True)
            return

        try:
            payment_amount = float(amount_field.value)
            if payment_amount <= 0:
                show_status("O valor deve ser positivo", is_error=True)
                return
        except ValueError:
            show_status("Valor inválido", is_error=True)
            return

        # Prepara os dados do pagamento
        payment_data = {
            "patient_id": patient_id,
            "professional_id": professional_id,
            "amount": payment_amount,
            "payment_method": payment_method.value
        }

        # Mostra loading e desabilita o botão
        loading_indicator.visible = True
        submit_button.disabled = True
        status_message.visible = False
        page.update()

        # Envia para a API
        response = api.create_payment(payment_data)

        # Processa a resposta
        if response.status_code == 200:
            show_status("Pagamento realizado com sucesso!")
            amount_field.value = ""
        else:
            error_msg = response.json().get("detail", "Erro ao processar pagamento")
            show_status(f"Erro: {error_msg}", is_error=True)

        # Esconde loading e reabilita o botão
        loading_indicator.visible = False
        submit_button.disabled = False
        page.update()

    def show_status(message, is_error=False):
        status_message.value = message
        status_message.color = ft.colors.RED if is_error else ft.colors.GREEN
        status_message.visible = True

    submit_button.on_click = process_payment

    # Layout da página
    content = ft.Column(
        [
            ft.Text("Realizar Pagamento", size=24, weight=ft.FontWeight.BOLD, color="#847769"),
            ft.Divider(height=20),
            amount_field,
            payment_method,
            ft.Container(height=10),
            submit_button,
            loading_indicator,
            status_message
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Barra inferior de navegação
    app_bar = ft.BottomAppBar(
        bgcolor="#847769",
        height=55,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOME, on_click=lambda e: page.go("/user"), icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.PAYMENT, icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
            ]
        ),
    )

    return ft.View(
        route="/make_payment",
        bgcolor="#f2dbc2",
        appbar=app_bar,
        controls=[content],
    )