import smtplib
from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from django.http import HttpResponse
from config.settings import EMAIL_HOST_USER
from edu_materials.models import Course
from .models import Subscription, User


@shared_task
def send_course_update_message(course_id):
    """Отправляет сообщение об обновлении материалов курса."""

    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course_id)
    recipient_list = [subscription.owner.email for subscription in subscriptions]

    try:
        send_mail(
            subject='В курсе произошли изменения',
            message=f'В курсе "{course.title}" произошли изменения',
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )
    except BadHeaderError:
        return HttpResponse('Обнаружен недопустимый заголовок.')
    except smtplib.SMTPException:
        raise smtplib.SMTPException


@shared_task
def send_course_update_for_update_lesson_message(lesson_id):
    """Отправляет сообщение об обновлении материалов урока курса."""

    course = Course.objects.get(lessons=lesson_id)
    subscriptions = Subscription.objects.filter(course=course.pk)
    recipient_list = [subscriptions.owner.email for subscriptions in subscriptions]

    try:
        send_mail(
            subject='В программе курса произошли изменения',
            message=f'В программе курса "{course.name}" произошли изменения',
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )
    except BadHeaderError:
        return HttpResponse('Обнаружен недопустимый заголовок.')
    except smtplib.SMTPException:
        raise smtplib.SMTPException


@shared_task
def blocking_inactive_users():
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
        return HttpResponse('Обнаружен недопустимый заголовок.')
    except smtplib.SMTPException:
        raise smtplib.SMTPException
    print(f"Отключены пользователи: {', '.join(users.email)}.")


@shared_task
def test_task(a, b):
    result = a + b
    print(result)
