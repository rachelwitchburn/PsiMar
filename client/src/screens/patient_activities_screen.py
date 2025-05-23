import flet as ft
from client.src.services import PsimarAPI


def patient_activities(page: ft.Page):
    token = page.session.get("token")
    if not token:
        page.go("/")
        return

    api = PsimarAPI(token=token)

    lista_tarefas = []

    def toggle_task_status(task_id: int, current_status: str):
        new_status = "completed" if current_status != "completed" else "pending"

        response = api.update_task_status(task_id, new_status)

        if response.status_code == 200:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Status da tarefa atualizado com sucesso!"),
                bgcolor=ft.colors.GREEN_400
            )
            load_tasks()  # Recarrega a lista de tarefas
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Erro ao atualizar tarefa"),
                bgcolor=ft.colors.RED_400
            )
        page.snack_bar.open = True
        page.update()

    def load_tasks():
        response = api.get_patient_tasks()

        lista_tarefas.clear()

        if response.status_code == 200:
            tasks = response.json()

            if not tasks:
                lista_tarefas.append(
                    ft.Text("Nenhuma tarefa disponível no momento.", size=16, color=ft.colors.GREY_700)
                )
            else:
                for task in tasks:
                    status_emoji = "✅ Concluída" if task["status"] == "completed" else "⏳ Pendente"
                    cor_status = ft.colors.GREEN_700 if task["status"] == "completed" else ft.colors.ORANGE_700
                    data_limite = (
                        f"Prazo: {task['due_date']}" if task.get("due_date") else "Sem prazo definido"
                    )

                    lista_tarefas.append(
                        ft.Container(
                            width=420,
                            padding=20,
                            margin=5,
                            bgcolor="#ffffff",
                            border_radius=10,
                            content=ft.Column([
                                ft.Text(task['title'], size=25, weight=ft.FontWeight.BOLD, color="#847769"),
                                ft.Text(task['description'], size=18, color="#847769"),
                                ft.Text(data_limite, size=14, color=ft.colors.GREY_700),
                                ft.Row([
                                    ft.Text(status_emoji, size=14, color=cor_status, italic=True),
                                    ft.IconButton(
                                        icon=ft.icons.CHECK_CIRCLE if task["status"] != "completed" else ft.icons.UNDO,
                                        icon_color=ft.colors.GREEN_700 if task[
                                                                              "status"] != "completed" else ft.colors.BLUE_700,
                                        on_click=lambda e, task_id=task["id"],
                                                        status=task["status"]: toggle_task_status(task_id, status),
                                        tooltip="Marcar como concluída" if task[
                                                                               "status"] != "completed" else "Marcar como pendente"
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                            ])
                        )
                    )
        else:
            lista_tarefas.append(
                ft.Text("Erro ao carregar tarefas.", color="red")
            )

        page.update()

    load_tasks()

    # Barra inferior
    appBar = ft.BottomAppBar(
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
        route="/",
        bgcolor="#f2dbc2",
        appbar=appBar,
        controls=[
            ft.Container(
                padding=ft.padding.only(top=20, left=20, right=20),
                content=ft.Row(
                    controls=[
                        ft.Text("Minhas Tarefas", size=25, weight=ft.FontWeight.BOLD, color="#847769"),

                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            ),
            ft.Divider(height=1),
            ft.Container(
                expand=True,
                alignment=ft.alignment.top_center,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=lista_tarefas
                )
            )
        ]
    )
