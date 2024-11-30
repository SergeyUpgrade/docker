from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from materials.models import Courses, Subscription
from users.models import User


@shared_task
def send_email_update_course(course_id):
    """ "
    Отправляет письмо с сообщением об изменении материалов курса
    """
    course = Courses.objects.get(id=course_id)
    message = f"Обновление материалов курса '{course.name}"
    users = User.objects.all()
    for user in users:
        subscription = Subscription.objects.filter(course=course, user=user.pk).exists()
        if subscription:
            send_mail(
                subject=f'Обновление курса "{course}"',
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )


@shared_task
def check_last_login():
    """
    Проверяет последний вход пользователей и отключает пользователей,
    не заходивших в последние 30 дней
    """
    users = User.objects.filter(last_login__isnull=False)
    today = timezone.now()
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f"Пользователь {user.email} отключен")
        else:
            print(f"Пользователь {user.email} активен")