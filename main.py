import threading
import schedule
from flask import Flask

from blueprints.task import task
from blueprints.user import user
from services.mail_services import MailServices
from services.task_database_service import TaskDatabaseService
from services.user_database_service import UserDatabaseService


def check_task_after_deadline():
    def check_deadline_daily():
        task_db = TaskDatabaseService()
        user_db = UserDatabaseService()

        tasks = task_db.get_task_after_deadline()
        mail_to_send = [(user_db.get_user_by_id(task_.user_id).email, task_.title, task_.deadline)
                        for task_ in tasks]
        if mail_to_send:
            mail_service = MailServices()
            mails = {}
            for mail in mail_to_send:
                if (user_email := mail[0]) in mails:
                    mails[user_email].append((mail[1], mail[2]))
                else:
                    mails[user_email] = []
                    mails[user_email].append((mail[1], mail[2]))
            for user_email, task_list in mails.items():
                mail_service.send_mail(user_email, task_list)

    def check_deadline():
        task_db = TaskDatabaseService()
        user_db = UserDatabaseService()

        tasks = task_db.get_task_after_deadline()
        mail_to_send = [(user_db.get_user_by_id(task_.user_id).email,
                         f"Deadline for {task_.title} has passed.",
                         task_.id)
                        for task_ in tasks
                        if task_ and not task_.notified]
        if mail_to_send:
            mail_service = MailServices()
            for mail in mail_to_send:
                mail_service.send_mail(mail[0], mail[1])
                task_db.update_task(mail[2], {"notified": True})

    schedule.every().day.at("00:00").do(check_deadline_daily)
    schedule.every(10).seconds.do(check_deadline)
    while True:
        schedule.run_pending()


def main():
    thread = threading.Thread(target=check_task_after_deadline)
    thread.start()
    app = Flask(__name__)
    app.register_blueprint(task)
    app.register_blueprint(user)
    app.config["TASK_DATABASE_SERVICE"] = TaskDatabaseService()
    app.config["USER_DATABASE_SERVICE"] = UserDatabaseService()
    app.config["SECRET_KEY"] = "random_key_47y9832y9nflsd"
    app.run()


if __name__ == '__main__':
    main()
