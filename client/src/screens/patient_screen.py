import flet as ft
from client.src.services import PsimarAPI


def patient(page):
    page.title = 'PsiMar'
    page.clean()

    token = page.session.get("token")
    print(token)

    if not token:
        print(" Nenhum token encontrado na sessão! Redirecionando para login...")
        page.go("/")
        return


    api = PsimarAPI(token=token)
    response= api.get_appointments()
    user_data = api.get_current_user()
    data_response = user_data.json()
    page.session.set("patient_id", data_response["id"])
    page.session.set("patient_first_name", data_response["first_name"])
    page.session.set("user_type", data_response["user_type"])
    patient_name = page.session.get("patient_first_name")





    lista_agendamentos = []

    if response.status_code == 200:
        agendamentos = response.json()
        if not agendamentos:
            lista_agendamentos.append(
                ft.Text("Nenhuma consulta agendada", color="#847769")
            )
        else:
            for agendamento in agendamentos:
                data_hora = agendamento["date_time"].replace("T", " ").split(".")[0]
                status = agendamento["status"]
                id_agendamento = agendamento["id"]

                card_controls = [
                    ft.Text(f"Consulta #{agendamento['id']}", size=25, weight=ft.FontWeight.BOLD, color="#847769"),
                    ft.Text(f"Data: {data_hora}", size=20, color="#847769"),
                    ft.Text(f"Status: {'Confirmado' if status == 'confirmed' else 'Pendente'}", size=20,
                            color="#847769"),
                ]

                if status == "confirmed":
                    payment_status = "pending"  # Você precisará obter isso da API depois

                    pay_button = ft.ElevatedButton(
                        "Pagar Consulta",
                        icon=ft.icons.PAYMENT,
                        bgcolor="#847769" if payment_status == "pending" else ft.colors.GREY_400,
                        color="white",
                        on_click=lambda e, ag=agendamento: store_appointment_data(page, ag),
                        width=200,
                        disabled=payment_status != "pending"
                    )
                    card_controls.append(pay_button)

                lista_agendamentos.append(
                    ft.Container(
                        content=ft.Column(card_controls),  # Aqui sim usamos ft.Column
                        width=420,
                        padding=20,
                        margin=5,
                        bgcolor="#ffffff",
                        border_radius=10
                    )
                )

                def store_appointment_data(page: ft.Page, agendamento: dict):
                    # Armazena cada informação separadamente na sessão
                    page.session.set("appointment_id", agendamento["id"])
                    page.session.set("patient_id", agendamento["patient_id"])
                    page.session.set("professional_id", agendamento["professional_id"])
                    page.go("/payment_user")

    def logout(page):
        page.session.remove("token")
        page.session.remove("patient_id")
        #print("Token após remoção:", page.session.get("token"))  # Deve imprimir None
        print("Token removido, fechando sessão")
        page.go("/")

    agendamentos = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        controls=lista_agendamentos
    )

    page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD)
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED


    appBar =  ft.BottomAppBar(
        bgcolor="#847769",
        height= 55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOUSE, icon_color= "white"),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.BOOK, on_click= lambda e: page.go("/patient_activities"),icon_color="white"),
                ft.Container(expand=True),
            ]
        ),
    )

    top_bar = ft.Container(
        padding=ft.padding.only(left=10, right=10, top=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    f"Olá, {patient_name}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#847769"
                ),
                ft.PopupMenuButton(
                    icon=ft.icons.MENU,
                    icon_color="#847769",
                    bgcolor="white",
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(ft.icons.WALLET, color="#847769"),
                                ft.Text("Realizar pagamentos", color="#847769"),
                            ]),
                            on_click=lambda e: page.go("/payment_user"),
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(ft.icons.FEEDBACK, color="#847769"),
                                ft.Text("Feedback", color="#847769"),
                            ]),
                            on_click=lambda e: page.go("/feedback_user"),
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(ft.icons.VIEW_AGENDA, color="#847769"),
                                ft.Text("Confirmar agendamentos", color="#847769"),
                            ]),
                            on_click=lambda e: page.go("/patient_confirm_appointment"),
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(ft.icons.LOCK, color="#847769"),
                                ft.Text("Redefinir senha", color="#847769"),
                            ]),
                            on_click=lambda e: page.go("/change_password"),
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(ft.icons.LOGOUT, color="#847769"),
                                ft.Text("Sair", color="#847769"),
                            ]),
                            on_click=lambda e: logout(page),
                        ),
                    ]
                )
            ]
        )
    )


    return ft.View(
        route="/user",
        bgcolor="#f2dbc2",
        appbar=appBar,
        controls=[
            top_bar,
            ft.Container(
                expand=True,
                alignment=ft.alignment.top_center,
                content=agendamentos,
            ),
        ],
        floating_action_button=ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=lambda e: page.go("/patient_appointment"),
            bgcolor= "#847769",
            foreground_color= "white",
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
)
