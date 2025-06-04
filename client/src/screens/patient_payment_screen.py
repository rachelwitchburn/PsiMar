import flet as ft

from client.src.services import PsimarAPI

def payment(page: ft.Page):
    page.title = "Realizar Pagamento"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#f2dbc2"
    page.padding = 20

    # Verifica autenticação
    token = page.session.get("token")
    appointment_id = page.session.get("appointment_id")
    patient_id = page.session.get("patient_id")
    professional_id = page.session.get("professional_id")

    print(f"ID da consulta: {appointment_id}")
    print(f"ID do paciente: {patient_id}")
    print(f"ID do profissional: {professional_id}")
    if not token:
        page.go("/")
        return

    api = PsimarAPI(token=token)

    # Elementos do formulário
    amount_field = ft.TextField(
        label="Valor",
        label_style= ft.TextStyle(color= "black"),
        prefix_text="R$ ",
        prefix_style= ft.TextStyle(color= "black"),
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color="#847769",
        width=300,
        text_size=16,
        color="black"
    )

    payment_method = ft.Dropdown(
        label="Método de Pagamento",
        label_style=ft.TextStyle(color="black"),
        color="black",
        border_color="#847769",
        width=300,
        bgcolor="white",
        options=[
            ft.dropdown.Option("card", "Cartão de Crédito"),
            ft.dropdown.Option("transfer", "Transferência Bancária"),
            ft.dropdown.Option("cash", "Dinheiro"),
        ],
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
            "appointment_id" : appointment_id,
            "patient_id": patient_id,
            "professional_id": professional_id,
            "amount": payment_amount,
            "payment_method": payment_method.value
        }
        print(payment_data)

        # Mostra loading e desabilita o botão
        loading_indicator.visible = True
        submit_button.disabled = True
        status_message.visible = False
        page.update()

        create_response = api.create_payment(payment_data)

        if create_response.status_code != 200:
            error_msg = create_response.json().get("detail", "Erro ao criar pagamento")
            show_status(f"Erro: {error_msg}", is_error=True)
            return

         #Se criação foi bem sucedida, obtém o ID do pagamento criado
        payment_id = create_response.json().get("id")
        if not payment_id:
            show_status("Erro: ID do pagamento não retornado", is_error=True)
            return

        # Confirma o pagamento
        confirm_response = api.confirm_payment(payment_id)

        if confirm_response.status_code == 200:
            show_status("Pagamento criado e confirmado com sucesso!")
            page.session.remove("appointment_id")
            page.session.remove("professional_id")
            page.session.remove("patient_id")
            amount_field.value = ""
            page.go("/patient")
        else:
            error_msg = confirm_response.json().get("detail", "Erro ao confirmar pagamento")
            show_status(f"Pagamento criado mas não confirmado: {error_msg}", is_error=True)

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
                ft.IconButton(icon=ft.icons.HOME, on_click=lambda e: page.go("/patient"), icon_color=ft.colors.WHITE),
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