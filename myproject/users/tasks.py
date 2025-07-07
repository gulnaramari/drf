import smtplib
from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse, BadHeaderError
from config.settings import EMAIL_HOST_USER
from edu_materials.models import Course
from .models import Subscription, User


@shared_task
def send_course_update(course_id):
    """Отправляет сообщение об обновлении материалов курса тем, кто подписан на этот курс."""

    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course_id)
    recipient_list = [subscription.owner.email for subscription in subscriptions]

    try:
        send_mail(
            subject='В курсе произошли изменения',
            message=f'В курсе "{course.name}" произошли изменения',
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )
    except smtplib.SMTPException:
        raise smtplib.SMTPException


@shared_task
def blocking_users():
    """Блокирует пользователей, которые бездействуют более 30 дней."""

    users = User.objects.filter(is_active=True)
    today = timezone.now()
    for user in users:
        if user.last_login:
            if today - user.last_login.date() > timedelta(days=30):
                user.is_active = False
                user.save()
    recipient_list = [user.email for user in User.objects.filter(groups='Администратор')]
    try:
        send_mail(
            subject='Блокировка неактивных пользователей',
            message=f"Пользователи: {', '.join(users.email)} заблокированы.",
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )
    except BadHeaderError:
        return HttpResponse('Обнаружена ошибка')
    except smtplib.SMTPException:
        raise smtplib.SMTPException
    print(f"Пользователи:{', '.join(users.email)} заблокированы.")







@shared_task
def add_test(a, b):
    result = a + b
    print(result)
