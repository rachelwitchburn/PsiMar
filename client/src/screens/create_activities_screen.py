import flet as ft
from datetime import datetime
from client.src.services import PsimarAPI


def create_activities(page: ft.Page):
    page.title = 'Criar Atividade'
    page.clean()

    # Obter token da sessão
    token = page.session.get("token")
    if not token:
        page.go("/")
        return

    api = PsimarAPI(token=token)

    # Elementos do formulário
    title = ft.TextField(
        label="Título",

        border_color="black",
        color="black",
        bgcolor="white",
        width=300,

    )

    description = ft.TextField(
        label="Descrição",
        border_color="black",
        color="black",
        bgcolor="white",
        width=300,
        multiline=True,
        min_lines=3,
        max_lines=5
    )

    due_date = ft.TextField(
        label="Data de Vencimento (DD/MM/AAAA)",
        border_color="black",
        color="black",
        bgcolor="white",
        width=300
    )

    patient_dropdown = ft.Dropdown(
        label="Paciente*",
        options=[],
        width=300,
        bgcolor= "white",
        border_color="black"
    )

    def load_patients():
        response = api.get_patients()
        if response.status_code == 200:
            patients = response.json()
            patient_dropdown.options = [
                ft.dropdown.Option(
                    text=f"{p['name']}", 
                    key=str(p['id'])
                ) for p in patients
            ]
            page.update()

    load_patients()

    # Criar tarefa
    def create_task(e):
        if not all([title.value, patient_dropdown.value]):
            page.snack_bar = ft.SnackBar(ft.Text("Preencha os campos obrigatórios*"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            task_data = {
                "title": title.value,
                "description": description.value,
                "patient_id": int(patient_dropdown.value),
                "due_date": datetime.strptime(due_date.value, "%d/%m/%Y").isoformat() if due_date.value else None
            }

            response = api.create_task(task_data)

            if response.status_code == 201:
                page.snack_bar = ft.SnackBar(ft.Text("Tarefa criada com sucesso!"))
                page.go("/professional_activities")
            else:
                error_msg = response.json().get("detail", "Erro ao criar tarefa")
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {error_msg}"))

            page.snack_bar.open = True
            page.update()

        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Formato de data inválido (use DD/MM/AAAA)"))
            page.snack_bar.open = True
            page.update()

    # Layout simplificado
    form = ft.Column(
        controls=[
            ft.Text("Criar Nova Tarefa", size=24, weight=ft.FontWeight.BOLD, color= "#847769"),
            title,
            description,
            patient_dropdown,  # Dropdown único e auto-carregável
            due_date,
            ft.ElevatedButton(
                "Criar Tarefa",
                on_click=create_task,
                icon=ft.icons.ADD,
                width=200,
                style=ft.ButtonStyle(
                    bgcolor="#847769",
                    color="white"
                )
            )
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return ft.View(
        route="/create_activities",
        controls=[
            ft.Container(
                content=form,
                padding=30,
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        bgcolor="#f2dbc2"
    )