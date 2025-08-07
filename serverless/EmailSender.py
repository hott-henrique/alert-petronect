import smtplib

from email.message import EmailMessage

import pathlib, typing as t

from projectconfig.ProjectConfig import ProjectConfig


class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.username = ProjectConfig.instance().email.user
        self.password = ProjectConfig.instance().email.password

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachments: list[tuple[str, bytes]] = [],
        html: bool = False
    ):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = to_email

        if html:
            msg.set_content("Este e-mail contém conteúdo em HTML. Use um cliente compatível para visualizar corretamente.")
            msg.add_alternative(body, subtype="html")
        else:
            msg.set_content(body)

        for filename, content in attachments:
            msg.add_attachment(
                content,
                maintype="application",
                subtype="octet-stream",
                filename=filename
            )

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.username, self.password)
            server.send_message(msg)
