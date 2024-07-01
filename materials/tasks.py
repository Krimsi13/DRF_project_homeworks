from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER

from materials.models import Subscription, Course


# 1ый вариант
# @shared_task
# def send_mail_of_update_course(email_list):
#     for email in email_list:
#         send_mail(
#             subject='Обновление курса',
#             message='Курс был обновлен',
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[email],
#         )


@shared_task
def send_mail_of_update_course(pk):
    course = Course.objects.get(pk=pk)
    subscribers = Subscription.objects.get(course=pk)

    send_mail(subject=f'Обновление курса.',
              message=f'Курс "{course}" был обновлен.',
              from_email=EMAIL_HOST_USER,
              recipient_list=[subscribers.user.email])
