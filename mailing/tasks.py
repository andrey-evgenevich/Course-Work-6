import logging
import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import Attempt, Mailing

logger = logging.getLogger("mailer")


def send_due_mailings():
    logger.info("Функция send_due_mailings запущена.")
    timezone.get_current_timezone()
    current_datetime = timezone.now()

    mailings = Mailing.objects.filter(
        date_time__lte=current_datetime, status__in=["created", "running"]
    )

    for mailing in mailings:
        try:
            send_mail(
                subject=mailing.message.topic,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()],
                fail_silently=False,
            )

            Attempt.objects.create(
                mailing=mailing,
                date_time=current_datetime,
                status=True,
                server_response="Письмо отправлено успешно",
            )

            logger.info(f"Рассылка {mailing.id} отправлена успешно.")

            if mailing.frequency == "once":
                mailing.status = "completed"
            else:
                mailing.status = "started"
                mailing.date_time = calculate_next_send_time(mailing, current_datetime)
            mailing.save()

        except smtplib.SMTPException as e:
            Attempt.objects.create(
                mailing=mailing,
                date_time=current_datetime,
                status=False,
                server_response=str(e),
            )

            logger.error(f"Ошибка при отправке рассылки {mailing.id}: {e}")

            mailing.status = "started"
            mailing.save()

        except Exception as e:
            Attempt.objects.create(
                mailing=mailing,
                date_time=current_datetime,
                status=False,
                server_response=str(e),
            )

            logger.error(f"Неизвестная ошибка при отправке рассылки {mailing.id}: {e}")

            mailing.status = "started"
            mailing.save()


def calculate_next_send_time(mailing, last_send_time):
    if mailing.frequency == "daily":
        return last_send_time + timezone.timedelta(days=1)
    elif mailing.frequency == "weekly":
        return last_send_time + timezone.timedelta(weeks=1)
    elif mailing.frequency == "monthly":
        return last_send_time + timezone.timedelta(days=30)
    else:
        return last_send_time
    