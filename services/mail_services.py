import smtplib


class MailServices:
    SENDER = "a@a.pl"

    def __init__(self):
        try:
            self.smtp_client = smtplib.SMTP('localhost')
        except ConnectionRefusedError:
            print("Can not connect to SMTP server.")
            self.smtp_client = None

    def send_mail(self, address, body):
        print(f"Mail from {self.SENDER} send to {address}")
        print(body)
        if self.smtp_client:
            try:
                self.smtp_client.sendmail(self.SENDER, address, body)
            except smtplib.SMTPException as ex:
                print(str(ex))
        else:
            print("Mail doesn't send because SMTP is not running.")
