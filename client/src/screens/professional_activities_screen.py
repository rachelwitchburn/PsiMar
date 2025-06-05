import flet as ft
from client.src.services import PsimarAPI

def professional_activities(page: ft.Page):
    # Obter token da sessão
    token = page.session.get("token")
    if not token:
        page.go("/")
        return

    api = PsimarAPI(token=token)
    response = api.get_assigned_tasks()

    lista_tarefas = []

    if response.status_code == 200:
        tarefas = response.json()
        if not tarefas:
            lista_tarefas.append(
                ft.Text("Nenhuma tarefa atribuída.")
            )
        else:
            for tarefa in tarefas:
                titulo = tarefa.get("title", "Sem título")
                descricao = tarefa.get("description", "Sem descrição")
                status = tarefa.get("status", "pendente")  # Exemplo de status
                data_limite = tarefa.get("due_date", "Sem data")  # Se existir esse campo

                lista_tarefas.append(
                    ft.Container(
                        width=420,
                        padding=20,
                        margin=5,
                        bgcolor="#ffffff",
                        border_radius=10,
                        content=ft.Column([
                            ft.Text(f"Título: {titulo}", size=22, weight=ft.FontWeight.BOLD, color="#847769"),
                            ft.Text(f"Descrição: {descricao}", size=18, color="#847769"),
                            ft.Text(f"Status: {"Pendente" if status == "pending" else "Completa"}", size=18, color="#847769"),
                            ft.Text(f"Prazo: {data_limite}", size=18, color="#847769"),
                        ])
                    )
                )
    else:
        lista_tarefas.append(
            ft.Text("Erro ao carregar tarefas", color="red")
        )

    appBar = ft.BottomAppBar(
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
                    icon_color=ft.colors.WHITE
                ),
                ft.Container(expand=True),
            ]
        ),
    )

    return ft.View(
        route="/professional_activities",
        bgcolor="#f2dbc2",
        appbar=appBar,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.top_center,
                padding=20,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=lista_tarefas,
                ),
            )
        ],
        floating_action_button=ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=lambda e: page.go("/create_activities"),
            bgcolor="#847769",
            foreground_color="white",
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )
