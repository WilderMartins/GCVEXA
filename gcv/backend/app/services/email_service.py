from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from ...core.config import settings
from ...models.scan import Scan

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=settings.SMTP_TLS,
    USE_CREDENTIALS=True if settings.SMTP_USER else False,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / '../templates/email'
)

fm = FastMail(conf)

async def send_scan_completion_email(scan: Scan):
    if not settings.SMTP_HOST:
        print("WARN: SMTP not configured. Skipping email notification.")
        return

    template_body = {
        "user_name": scan.user.full_name or scan.user.email,
        "target": scan.target_host,
        "scan_id": scan.id,
        "vulnerability_count": len(scan.vulnerabilities),
        # Idealmente, teríamos a URL base do frontend nas configurações
        "scan_url": f"http://localhost:5173/scans/{scan.id}"
    }

    message = MessageSchema(
        subject=f"GCV Scan Completed for {scan.target_host}",
        recipients=[scan.user.email],
        template_body=template_body,
        subtype="html"
    )

    try:
        await fm.send_message(message, template_name="scan_completed.html")
        print(f"Scan completion email sent to {scan.user.email}")
    except Exception as e:
        print(f"Error sending email: {e}")
