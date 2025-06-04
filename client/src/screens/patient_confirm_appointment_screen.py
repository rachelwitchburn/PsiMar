import flet as ft
from client.src.services import PsimarAPI

def confirm_appointment_patient(page: ft.Page):
    token = page.session.get("token")


    if not token:
        print("Nenhum token encontrado na sessão! Redirecionando para login...")
        page.go("/")
        return

    api = PsimarAPI(token=token)
    response = api.get_appointments()

    lista_widgets = []



    if response.status_code == 200:
        agendamentos = response.json()

        agendamentos_pendentes = [
            ag for ag in agendamentos if ag["status"] == "requested"
        ]

        if not agendamentos_pendentes:
            lista_widgets.append(ft.Text("Nenhum agendamento pendente.", color="black"))
        else:
            for ag in agendamentos_pendentes:
                agendamento_id = ag["id"]
                data_hora = ag["date_time"]
                paciente_id = ag["patient_id"]

                def confirmar_click(e, ag_id=ag["id"]):
                    resp = api.confirm_appointment_by_patient(ag_id)

                    if resp.status_code == 200:
                        print(f" Agendamento {agendamento_id} confirmado.")
                        page.go("/patient")  # Atualiza a tela
                    else:
                        print(f" Erro ao confirmar: {resp.text}")

                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Paciente ID: {paciente_id}", color="black"),
                            ft.Text(f"Data/Hora: {data_hora}", color="black"),
                            ft.ElevatedButton(
                                text="Confirmar",
                                on_click=confirmar_click
                            )
                        ]),
                        padding=10,
                        bgcolor="#f5f5f5",
                        border_radius=10
                    )
                )
                lista_widgets.append(card)
    else:
        lista_widgets.append(ft.Text("Erro ao carregar agendamentos.", color="red"))

    return ft.View(
        route="/patient_confirm_appointment",
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            on_click=lambda e: page.go("/patient"),
                            icon_color="black",
                        ),
                        alignment=ft.alignment.top_left
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            *lista_widgets
        ],
        bgcolor="#f2dbc2"
    )


