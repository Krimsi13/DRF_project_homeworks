from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Email", max_length=255)
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона"
    )
    city = models.CharField(
        max_length=255,
        verbose_name="Страна",
        **NULLABLE,
        help_text="Введите свою страну"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите свой аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    METHODS = (
        ("cash", "Наличными"),
        ("transfer", "Перевод на счёт"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments", verbose_name="Пользователь"
    )
    date_of_payment = models.DateField(auto_now_add=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments",
                               verbose_name="Оплаченный курс", **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="payments",
                               verbose_name="Оплаченный урок", **NULLABLE)

    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")

    payment_method = models.CharField(choices=METHODS, max_length=20, verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
