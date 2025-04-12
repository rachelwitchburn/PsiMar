import flet as ft
from flet_core import FontWeight


def register(page):
    page.title = 'PsiMar'

    Senha = ft.Ref[ft.TextField]()  # Correção: Inicializa sem passar um valor aqui

    def toggle_password(e):
        senha_field = Senha.current
        senha_field.password = not senha_field.password
        senha_field.suffix.icon = ft.icons.VISIBILITY if senha_field.password else ft.icons.VISIBILITY_OFF
        page.update()

    def show_form(tipo):
        form_container.clean()

        if tipo == "psicologo":
            form_container.content = psicologo_form()
        else:
            form_container.content = paciente_form()

        page.update()

    # A checkbox para aceitar os termos -> TIRAR
    def handle_close(e):
        page.close(dlg)

    dlg = ft.AlertDialog(modal=True,
                         title=ft.Text("Termos de uso"),
                         content=ft.Column([
                             ft.Text("Texto dos termos aqui"),
                             ft.Checkbox(
                                 label="Aceito os termos de uso",
                             ),
                         ]),
                         actions=[

                             ft.TextButton("Fechar", on_click=handle_close),
                         ],
                         actions_alignment=ft.MainAxisAlignment.END,
                         on_dismiss=lambda e: page.add(
                             ft.Text("Modal dialog dismissed"),
                         ),
                         )

    def psicologo_form():
        return ft.Column([
            ft.TextField(
                label="Código",
                label_style=ft.TextStyle(color="black"),
                width=300,
                border_color="black",
                color="black",
                bgcolor="white"
            ),
            ft.TextField(
                ref=Senha,
                label="Senha",
                label_style=ft.TextStyle(color="black"),
                password=True,
                width=300,
                border_color="black",
                color="black",
                bgcolor="white",
                suffix=ft.IconButton(
                    icon=ft.icons.VISIBILITY_OFF,
                    icon_color="black",
                    on_click=toggle_password
                )
            ),
            ft.TextButton("Termos de uso", on_click=lambda e: page.open(dlg)),
            ft.ElevatedButton(
                "Registrar",
                on_click=lambda e: page.go("/psicologo"),
                width=150,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5),
                    elevation=5,
                    overlay_color="rgba(255, 255, 255, 0.2)",
                    bgcolor="black",
                    color="white"
                )
            )
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def paciente_form():
        return ft.Column([
            ft.TextField(
                label="Código",
                label_style=ft.TextStyle(color="black"),
                width=300,
                border_color="black",
                color="black",
                bgcolor="white"
            ),
            ft.TextField(
                ref=Senha,
                label="Senha",
                label_style=ft.TextStyle(color="black"),
                password=True,
                width=300,
                border_color="black",
                color="black",
                bgcolor="white",
                suffix=ft.IconButton(
                    icon=ft.icons.VISIBILITY_OFF,
                    icon_color="black",
                    on_click=toggle_password
                )
            ),
            ft.TextButton("Termos de uso", on_click=lambda e: page.open(dlg)),
            ft.ElevatedButton(
                "Registrar",
                on_click=lambda e: page.go("/usuario"),
                width=150,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5),
                    elevation=5,
                    overlay_color="rgba(255, 255, 255, 0.2)",
                    bgcolor="black",
                    color="white"
                )
            )
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    form_container = ft.Container()

    return ft.View(
        route="/register",
        bgcolor="#f2dbc2",
        controls=[
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: page.go("/"),
                    icon_color="black",
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10, top=10),
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Escolha seu perfil:", size=20, weight=FontWeight.BOLD, color="black"),
                    ft.Row([
                        ft.ElevatedButton("Sou Psicólogo", on_click=lambda e: show_form("psicologo"),
                                          style=ft.ButtonStyle(
                                              shape=ft.RoundedRectangleBorder(radius=5),
                                              elevation=5,
                                              overlay_color="rgba(255, 255, 255, 0.2)",
                                              bgcolor="black",
                                              color="white"
                                          )),
                        ft.ElevatedButton("Sou Paciente", on_click=lambda e: show_form("paciente"),
                                          style=ft.ButtonStyle(
                                              shape=ft.RoundedRectangleBorder(radius=5),
                                              elevation=5,
                                              overlay_color="rgba(255, 255, 255, 0.2)",
                                              bgcolor="black",
                                              color="white"
                                          )),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    form_container,
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                expand=True
            )
        ]
    )
