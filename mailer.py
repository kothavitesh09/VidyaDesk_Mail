import os
import requests


BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def configure_mail(app):
    pass


def send_plain_email(recipient: str, subject: str, body: str):

    api_key = os.getenv("BREVO_API_KEY")

    if not api_key:
        raise RuntimeError("BREVO_API_KEY is not configured")

    sender_email = os.getenv("SENDER_EMAIL")

    if not sender_email:
        raise RuntimeError("SENDER_EMAIL is not configured")

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": "VidyaDesk",
            "email": sender_email,
        },
        "to": [
            {
                "email": recipient
            }
        ],
        "subject": subject,
        "textContent": body,
    }

    response = requests.post(
        BREVO_API_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Brevo API Error: {response.status_code} - {response.text}"
        )

    return response.json()
