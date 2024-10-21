import base64
import logging

from core.tasks import send_core_email
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment
from sendgrid.helpers.mail import Disposition
from sendgrid.helpers.mail import FileContent
from sendgrid.helpers.mail import FileName
from sendgrid.helpers.mail import FileType
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


class EmailService:
    def send_email(self, subject, body, to_emails, attachments=None):
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


class CoreService:
    def __init__(self, sendgrid_service=None) -> None:
        self.sendgrid_service = sendgrid_service

    def send_email(
        self,
        subject,
        template_path,
        template_context,
        to_emails,
        attachments=None,
    ):
        """SEND EMAIL"""

        # if settings.DEBUG:
        #     print(f"Sending email to {to_emails}")
        #     return

        self.sendgrid_service
        send_core_email(
            subject=subject,
            template_path=template_path,
            template_context=template_context,
            to_emails=to_emails,
            attachments=attachments,
        )
