from datetime import datetime

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from edu_materials.models import Course, Lesson


class UserManager(BaseUserManager):
    """Создает пользователя или суперпользователя с нужными правами"""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("У пользователя должна быть почта")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Создание модели пользователя с соответствующими полями"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="Введите почту"
    )

    phone = models.CharField(
        max_length=35,
        verbose_name="телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="аватар",
        blank=True,
        null=True,
        help_text="Загрузите аватар",
    )
    town = models.CharField(
        max_length=35,
        verbose_name="город",
        blank=True,
        null=True,
        help_text="Введите название города",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="staff",
        help_text="Select whether user can act as admin",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="active",
        help_text="Select whether user can use the service",
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Создание модели платежа с соответствующими полями"""

    PAYMENT_CHOICES = [
        ("BANK_TRANSFER", "Банковский перевод"),
        ("CASH", "Наличными"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="пользователь",
        help_text="выберите пользователя",
        null=True,
        blank=True,
    )
    payment_date = models.DateTimeField(default=datetime.now, verbose_name="Дата оплаты",
                                    help_text="Введите дату платежа")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        help_text = "Выберите курс",
        related_name="payments",
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        related_name="payments",
        help_text="Выберите лекцию",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        decimal_places=2, max_digits=20,
        verbose_name="Сумма платежа",
        help_text="Введите сумму платежа",
        validators=[MinValueValidator(0)],
    )
    payment_type = models.CharField(
        max_length=50, choices=PAYMENT_CHOICES,
        default="BANK_TRANSFER",
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты"
    )

    def __str__(self):
        return f"Payment for {self. paid_course} by {self.user.email}"

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"