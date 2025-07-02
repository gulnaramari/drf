import re
from rest_framework.serializers import ValidationError


class URLValidator:
    """Класс для валидации ссылок на курс."""

    def __init__(self, field):
        """Метод для инициализации объекта класса."""
        self.field = field

    def __call__(self, value):
        """Метод для поверки данных поля ссылки"""
        reg = re.compile("^(https?://)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]*$")

        tmp_value = dict(value).get(self.field)

        if not value or value is None or not bool(reg.match(tmp_value)):
            raise ValidationError("Введите правильную ссылку")
        elif "youtube.com" not in tmp_value:
            raise ValidationError(
                "Ссылка на видео разрешена только с сайта youtube.com"
            )
