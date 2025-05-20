import smtplib
from email.message import EmailMessage

def send_payment_email(to_email: str, amount: float):
    msg = EmailMessage()
    msg["Subject"] = "Pagamento pendente - PsiMar"
    msg["From"] = "seuemail@gmail.com"
    msg["To"] = to_email
    msg.set_content(f"""
Olá,
Você tem um pagamento pendente no valor de R${amount:.2f} referente à sua consulta.
Por favor, realize o pagamento e aguarde a confirmação do seu psicólogo.
Atenciosamente, Maria, sua psi.
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("seuemail@gmail.com", "senha_de_app")  # Use senha de app!
        smtp.send_message(msg)
