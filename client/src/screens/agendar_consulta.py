import flet as ft

def agendar_consulta(page):
    

    return ft.View(
        route="/usuario",
        bgcolor="#f2dbc2",
       
        controls=[
            ft.Column(
                expand=True, 
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls = [
                    ft.Container(
                        alignment= ft.alignment.center,
                        content= ft.Text("Criar a agenda aqui!", color= "black")
                    )
                ]

            ),

         
        ],

)