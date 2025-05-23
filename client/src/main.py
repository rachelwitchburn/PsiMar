import flet as ft

from services import PsimarAPI
from screens.login_screen import login
from screens.professional_screen import psychologist
from screens.register_screen import register
from screens.user_screen import user
from screens.change_password_screen import change_password
from screens.patient_activities_screen import patient_activities
from screens.professional_activities_screen import professional_activities
from screens.patient_make_appointment_screen import make_appointment_patient
from screens.professional_make_appointment_screen import make_appointment_professional
from screens.create_activities_screen import create_activities
from screens.feedback_user_screen import create_feedback
from screens.feedback_professional_screen import read_feedbacks
from screens.professional_confirm_appointment_screen import confirm_appointment
from screens.patient_confirm_appointment_screen import confirm_appointment


def main(page: ft.Page):
    page.title = "PsiMar"
    page.window_maximized = True

    page.client = PsimarAPI()


# funcao que troca rotas pro usuario

    routes = {
        "/": login,
        "/register": register,
        "/user": user,
        "/professional": psychologist,
        "/changePass": change_password,
        "/patient_activities": patient_activities,
        "/professional_activities": professional_activities,
        "/patient_appointment": make_appointment_patient,
        "/professional_appointment": make_appointment_professional,
        "/professional_confirm_appointment": confirm_appointment,
        "/patient_confirm_appointment": confirm_appointment,
        "/create_activities": create_activities,
        "/feedback_user": create_feedback,
        "/feedback_professional": read_feedbacks


    }

    def route_change(route):
        page.views.clear()
        view_fn = routes.get(page.route, lambda p: ft.View(route, [ft.Text("Página não encontrada")]))
        page.views.append(view_fn(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")


ft.app(main, view=ft.AppView.FLET_APP)
