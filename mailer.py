import os

from flask_mail import Mail, Message


mail = Mail()


def configure_mail(app):
    app.config.update(
        MAIL_SERVER="smtp.gmail.com",
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME"),
    )
    mail.init_app(app)


def send_plain_email(recipient: str, subject: str, body: str) -> None:
    if not os.getenv("MAIL_USERNAME") or not os.getenv("MAIL_PASSWORD"):
        raise RuntimeError("MAIL_USERNAME and MAIL_PASSWORD must be configured")

    message = Message(subject=subject, recipients=[recipient], body=body)
    mail.send(message)
