import flet as ft
from datetime import datetime, timedelta ,timezone
from client.src.services import PsimarAPI


def make_appointment_patient(page: ft.Page):
    page.title = 'Agendar Consulta'
    page.clean()

    # Obter o token da sessão
    token = page.session.get("token")
    patient_id = page.session.get("user_id")
    if not token:
        page.go("/")
        return

    api = PsimarAPI(token=token)
    professional_id = 9

    # Variáveis para seleção
    selected_date = None
    selected_time = None

    go_back = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda e: page.go("/user"),
        icon_color="black",
    )

    title = ft.Text("Agendar Nova Consulta", size=24, weight=ft.FontWeight.BOLD, color= "#847769")

    def build_date_picker():
        today = datetime.now().date()
        next_week = today + timedelta(days=7)

        dates = []
        current_date = today
        while current_date <= next_week:
            if current_date.weekday() < 5:  # Apenas dias úteis
                dates.append(current_date)
            current_date += timedelta(days=1)

        return ft.Row(
            controls=[
                ft.ElevatedButton(
                    text=date.strftime("%a\n%d/%m"),
                    data=date,
                    on_click=lambda e: select_date(e.control.data),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor=ft.colors.WHITE,
                        color = "#847769"
                    ),
                    width=80,
                    height=80,
                ) for date in dates
            ],
            scroll="auto",
        )

    date_picker = build_date_picker()

    # Horários disponíveis
    time_buttons = ft.Row(
        controls=[
            ft.ElevatedButton(
                text=time,
                data=time,
                on_click=lambda e: select_time(e.control.data),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    bgcolor=ft.colors.WHITE,
                    color= "#847769"
                ),
                width=100,
            ) for time in ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        ],
        spacing=10,
        scroll="auto",  # Adicione scroll se os botões não couberem na tela
        wrap=True,
    )

    # Funções de seleção
    def select_date(date):
        nonlocal selected_date
        selected_date = date
        # Atualiza visual dos botões
        for btn in date_picker.controls:
            btn.bgcolor = ft.colors.WHITE if btn.data != date else "#847769"
            btn.color = "black" if btn.data != date else "white"
        page.update()

    def select_time(time):
        nonlocal selected_time
        selected_time = time
        # Atualiza visual dos botões
        for btn in time_buttons.controls:
            btn.bgcolor = ft.colors.WHITE if btn.data != time else "#847769"
            btn.color = "black" if btn.data != time else "white"
        page.update()

    # Função para enviar agendamento
    def submit_appointment(e):
        if not selected_date or not selected_time:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione data e horário!"))
            page.snack_bar.open = True
            page.update()
            return

        # Parse hora e minuto da string selected_time
        hour, minute = map(int, selected_time.split(":"))

        # Cria datetime com timezone UTC
        appointment_datetime = datetime(
            year=selected_date.year,
            month=selected_date.month,
            day=selected_date.day,
            hour=hour,
            minute=minute,
            tzinfo=timezone.utc,
        )

        p_id = patient_id
        response = api.create_appointment(professional_id, p_id, appointment_datetime.isoformat())

        print("Enviando:", appointment_datetime.isoformat())

        print("STATUS:", response.status_code)
        print("RESPONSE TEXT:", response.text)

        if response.status_code == 200:
            page.snack_bar = ft.SnackBar(ft.Text("Consulta agendada com sucesso!"))
            page.go("/user")
        else:
            error_msg = response.json().get("detail", "Erro desconhecido")
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {error_msg}"))

        page.snack_bar.open = True
        page.update()

    content = ft.Column(
        controls=[
            ft.Row([go_back], alignment="start"),
            title,
            ft.Text("Selecione o dia:", size=16, color="#847769"),
            date_picker,
            ft.Text("Selecione o horário:", size=16, color= "#847769"),
            time_buttons,
            ft.ElevatedButton(
                "Confirmar Agendamento",
                on_click=submit_appointment,
                bgcolor="#847769",
                color="white",
                width=200,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5),
                    elevation=5,
                    overlay_color="rgba(255, 255, 255, 0.2)",
                    bgcolor="#212121",
                    color="white")
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        route="/make_appointment",
        bgcolor="#f2dbc2",
        padding=20,
        controls=[content],
    )