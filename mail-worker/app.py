import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from mailer import configure_mail, send_plain_email


app = Flask(__name__)

allowed_origin = os.getenv("VIDYADESK_VERCEL_DOMAIN", "https://vidyadesk.vercel.app")
CORS(app, resources={r"/send-email": {"origins": [allowed_origin]}})

configure_mail(app)


def _authorized() -> bool:
    api_key = os.getenv("MAIL_API_KEY")
    auth_header = request.headers.get("Authorization", "")

    if not api_key:
        return False

    return auth_header == f"Bearer {api_key}"


@app.post("/send-email")
def send_email():
    if not _authorized():
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    payload = request.get_json(silent=True) or {}
    recipient = payload.get("to")
    subject = payload.get("subject")
    body = payload.get("body")

    if not recipient or not subject or not body:
        return jsonify({"success": False, "error": "to, subject, and body are required"}), 400

    try:
        send_plain_email(recipient, subject, body)
        return jsonify({"success": True, "message": "Email sent"}), 200
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@app.get("/health")
def health():
    return jsonify({"success": True, "message": "Mail worker healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
