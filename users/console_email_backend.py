import logging
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)


class ConsoleEmailBackend(BaseEmailBackend):
    """
    A console email backend for development and testing purposes.
    This backend writes email messages to the console instead of sending them.
    """

    def send_messages(self, email_messages):
        """
        Write the email messages to the console.

        Args:
            email_messages (list): A list of EmailMessage instances.

        Returns:
            int: The number of email messages "sent".
        """
        for message in email_messages:
            lines = [
                "-" * 40,
                f"Subject : {message.subject}",
                f"From    : {message.from_email}",
                f"To      : {', '.join(message.to)}",
            ]
            if message.cc:
                lines.append(f"CC      : {', '.join(message.cc)}")
            if message.bcc:
                lines.append(f"BCC     : {', '.join(message.bcc)}")
            lines += ["-" * 40, message.body, "-" * 40]
            logger.info("\n%s", "\n".join(lines))

        return len(email_messages)
