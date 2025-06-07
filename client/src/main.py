import flet as ft

from client.src.services import PsimarAPI
from client.src.screens.login_screen import login
from client.src.screens.professional_screen import psychologist
from client.src.screens.register_screen import register
from client.src.screens.patient_screen import patient
from client.src.screens.change_password_screen import change_password
from client.src.screens.patient_activities_screen import patient_activities
from client.src.screens.professional_activities_screen import professional_activities
from client.src.screens.patient_make_appointment_screen import make_appointment_patient
from client.src.screens.professional_make_appointment_screen import make_appointment_professional
from client.src.screens.create_activities_screen import create_activities
from client.src.screens.feedback_user_screen import create_feedback
from client.src.screens.feedback_professional_screen import read_feedbacks
from client.src.screens.professional_confirm_appointment_screen import confirm_appointment_professional
from client.src.screens.patient_confirm_appointment_screen import confirm_appointment_patient
from client.src.screens.patient_payment_screen import payment
from client.src.screens.professional_payment_screen import  payments_view



def main(page: ft.Page):
    page.title = "PsiMar"
    page.window_maximized = True

    page.client = PsimarAPI()


# funcao que troca rotas pro usuario

    routes = {
        "/": login,
        "/register": register,
        "/patient": patient,
        "/professional": psychologist,
        "/change_password": change_password,
        "/patient_activities": patient_activities,
        "/professional_activities": professional_activities,
        "/patient_appointment": make_appointment_patient,
        "/professional_appointment": make_appointment_professional,
        "/professional_confirm_appointment": confirm_appointment_professional,
        "/patient_confirm_appointment": confirm_appointment_patient,
        "/create_activities": create_activities,
        "/feedback_user": create_feedback,
        "/feedback_professional": read_feedbacks,
        "/payment_user": payment,
        "/payment_psychologist": payments_view


    }

    def route_change(route):
        page.views.clear()
        view_fn = routes.get(page.route, lambda p: ft.View(route, [ft.Text("Página não encontrada")]))
        page.views.append(view_fn(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")


ft.app(main, view=ft.AppView.FLET_APP)
