import flet as ft

def read_feedbacks(page):
    response = page.client.get_payments()
    payments_data = response.json() if response.status_code == 200 else []

    def confirmar_pagamento(e, payment_id):
        confirm_resp = page.client.confirm_payment(payment_id)
        if confirm_resp.status_code == 200:
            page.snack_bar = ft.SnackBar(
                ft.Text("Pagamento confirmado com sucesso!"), open=True
            )
            # Atualiza a tela após confirmar
            page.go("/feedback_professional")
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Erro ao confirmar o pagamento."), open=True
            )
        page.update()

    pagamentos_widgets = []

    for p in payments_data:
        if p["status"] == "pending":
            pagamentos_widgets.append(
                ft.Container(
                    margin=10,
                    padding=15,
                    bgcolor="#f5e6d4",
                    border_radius=10,
                    content=ft.Column([
                        ft.Text(f"Paciente ID: {p['patient_id']}", size=16, weight="bold", color="black"),
                        ft.Text(f"Valor: R$ {float(p['amount']):.2f}", size=14, color="black"),
                        ft.Text(f"Método: {p['payment_method']}", size=14, color="black"),
                        ft.Row([
                            ft.ElevatedButton(
                                text="Confirmar Pagamento",
                                bgcolor="#4CAF50",
                                color="white",
                                on_click=lambda e, pid=p["id"]: confirmar_pagamento(e, pid),
                            )
                        ])
                    ])
                )
            )

    if not pagamentos_widgets:
        pagamentos_widgets.append(
            ft.Text("Nenhum pagamento pendente.", size=16, color="black")
        )

    # AppBar e View
    appBar = ft.BottomAppBar(
        bgcolor="#847769",
        height=55.0,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOUSE, on_click=lambda e: page.go("/professional"),
                              icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.ATTACH_MONEY, icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
            ]
        ),
    )

    return ft.View(
        route="/feedback_professional",
        bgcolor="#f2dbc2",
        appbar=appBar,
        controls=[
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text("Pagamentos Pendentes", size=22, weight="bold", color="black", text_align="center"),
                    *pagamentos_widgets,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]
    )