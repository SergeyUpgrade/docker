from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Courses, Lessons


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )

    city = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Ваш аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    payment_date = models.DateField(verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, verbose_name="Оплаченный курс"
    )
    separately_paid_lesson = models.ForeignKey(
        Lessons,
        on_delete=models.CASCADE,
        verbose_name="Отдельно оплаченный урок"
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
    )

    def __str__(self):
        return f"{self.user} - {self.payment_amount} - {self.payment_date}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
