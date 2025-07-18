from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создает суперпользователя с нужными правами"

    def handle(self, *args, **kwargs):
        user = User.objects.create(email="admin@example.com")
        user.set_password("12345")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
