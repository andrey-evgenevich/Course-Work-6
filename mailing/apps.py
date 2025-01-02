from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"

    def ready(self):
        import time

        from .apscheduler import start

        time.sleep(2)
        start()
