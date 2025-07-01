import httpx
import smtplib
import base64
from src.app.shared.constants.settings import Settings
from email.message import EmailMessage

async def send_sms_token(phone_number: str, code: str) -> dict:
    try:
        url = Settings.CELL_URL + 'sms/1/text/single'
        username = Settings.CELL_USERNAME
        password = Settings.CELL_PASSWORD
        sender = Settings.CELL_CODE

        auth = f"{username}:{password}"
        basic_auth = base64.b64encode(auth.encode()).decode()

        headers = {
            "Authorization": f"Basic {basic_auth}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": "57" + phone_number,  # Colombia
            "from": sender,
            "text": f"Su código de verificación es: {code}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
        data = response.json()

        if response.status_code != 200:
            return {
                "status": "error",
                "message": "Error al procesar la respuesta del servidor.",
                "response": data
            }

        status_info = data['messages'][0]['status']
        if status_info['groupId'] not in [1, 3]:
            return {
                "status": "error",
                "message": status_info['name'],
                "details": data
            }

        return {
            "status": "success",
            "message": "SMS enviado correctamente.",
            "data": data
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

async def send_email_token(to_email: str, code: str, subject: str="Código de verificación") -> dict:
    try:
        mail_host = Settings.MAIL_HOST
        mail_port = int(Settings.MAIL_PORT)
        mail_user = Settings.MAIL_USERNAME
        mail_pass = Settings.MAIL_PASSWORD
        mail_from = Settings.MAIL_FROM_ADDRESS
        mail_name = Settings.MAIL_FROM_NAME
        mail_encryption = Settings.MAIL_ENCRYPTION

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = f"{mail_name} <{mail_from}>"
        msg['To'] = to_email
        msg.set_content(f"{code}")

        if mail_encryption == "ssl":
            server = smtplib.SMTP_SSL(mail_host, mail_port)
        else:
            server = smtplib.SMTP(mail_host, mail_port)
            server.starttls()

        server.login(mail_user, mail_pass)
        server.send_message(msg)
        server.quit()

        return {
            "status": "success",
            "message": "Correo enviado correctamente."
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}