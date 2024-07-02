from datetime import datetime, timezone, timedelta
from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER

from materials.models import Subscription, Course

from users.models import User


# Вариант №1
# @shared_task
# def send_mail_of_update_course(email_list):
#     for email in email_list:
#         send_mail(
#             subject='Обновление курса',
#             message='Курс был обновлен',
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[email],
#         )

# Вариант №2
# @shared_task
# def send_mail_of_update_course(pk):
#     course = Course.objects.get(pk=pk)
#     subscribers = Subscription.objects.get(course=pk)
#
#     send_mail(subject=f'Обновление курса.',
#               message=f'Курс "{course}" был обновлен.',
#               from_email=EMAIL_HOST_USER,
#               recipient_list=[subscribers.user.email])

# Вариант №3
@shared_task
def send_mail_of_update_course(pk):
    course = Course.objects.get(id=pk)
    subscribers = Subscription.objects.filter(course=course)
    email_list = [subscriber.user.email for subscriber in subscribers]

    for email in email_list:
        send_mail(subject=f'Обновление курса.',
                  message=f'Курс "{course}" был обновлен.',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[email])


@shared_task
def check_activity_user():
    is_active_users = User.objects.filter(is_active=True)
    current_time = datetime.now(timezone.utc)

    for user in is_active_users:
        if user.last_login:
            if current_time - user.last_login > timedelta(days=30):
                user.is_active = False
                user.save()
