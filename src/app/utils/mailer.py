import os
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
import aiosmtplib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

async def send_email(to_email: str,subject: str,template_name: str,context: dict):
    # Renderizar HTML
    template = env.get_template(template_name)
    html_content = template.render(context)

    # Crear mensaje
    message = EmailMessage()
    message["From"] = os.getenv("SMTP_SENDER_EMAIL")
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content("Este correo requiere un cliente que soporte HTML.")
    message.add_alternative(html_content, subtype='html')

    # Enviar email
    await aiosmtplib.send(
    message,
    hostname=os.getenv("MAIL_HOST"),
    port=int(os.getenv("MAIL_PORT")),
    start_tls=True,
    username=os.getenv("MAIL_USERNAME"),
    password=os.getenv("MAIL_PASSWORD"),
    )
