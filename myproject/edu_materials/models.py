from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="название курса",
        help_text="укажите название курса",
    )
    preview = models.ImageField(
        upload_to="edu_materials/previews",
        verbose_name="превью",
        blank=True,
        null=True,
        help_text="Загрузите превью",
    )
    description = models.TextField(
        max_length=250,
        verbose_name="описание курса",
        help_text="опишите курс",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="название урока",
        help_text="укажите название урока",
    )
    description = models.TextField(
        max_length=250,
        verbose_name="описание урока",
        help_text="опишите урок",
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        upload_to="edu_materials/pictures",
        verbose_name="картинка",
        blank=True,
        null=True,
        help_text="Загрузите изображение",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс",
        help_text="выберите курс",
        related_name="lesson_set",
    )
    video_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="ссылка на видео",
        help_text="загрузите видео",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
