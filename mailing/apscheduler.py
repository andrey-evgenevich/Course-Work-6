from apscheduler.schedulers.background import BackgroundScheduler

from mailing.tasks import send_due_mailings


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_due_mailings, "interval", seconds=10)
    scheduler.start()