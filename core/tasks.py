import base64
import logging

from django.conf import settings
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment
from sendgrid.helpers.mail import Disposition
from sendgrid.helpers.mail import FileContent
from sendgrid.helpers.mail import FileName
from sendgrid.helpers.mail import FileType
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


def send_email_via_sendgrid(subject, body, to_emails, attachments=None):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_emails,
        subject=subject,
        html_content=body,
    )

    if attachments:
        for attachment in attachments:
            encoded_file = base64.b64encode(
                attachment["file_content"]).decode()
            attached_file = Attachment(
                FileContent(encoded_file),
                FileName(attachment["filename"]),
                FileType("application/octet-stream"),
                Disposition("attachment"),
            )
            message.add_attachment(attached_file)

    try:
        sg = SendGridAPIClient(settings.SENDGRID_KEY)
        sg.send(message)
    except Exception as e:
        logger.error(f"Error sending email: {e}")


def send_core_email(
    subject, template_path, template_context, to_emails, attachments=None
):
    html_content = render_to_string(template_path, template_context)
    send_email_via_sendgrid(
        subject=subject,
        body=html_content,
        to_emails=to_emails,
        attachments=attachments,
    )
