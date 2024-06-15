from django.db import models

# from users.models import User
from config import settings

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials/preview/", **NULLABLE, verbose_name="Картинка"
    )
    description = models.TextField(verbose_name="Описание курса")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец", help_text="Укажите владельца курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока")
    preview = models.ImageField(
        upload_to="materials/preview/", **NULLABLE, verbose_name="Картинка"
    )
    link_to_video = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс", **NULLABLE
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец", help_text="Укажите владельца урока")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"



