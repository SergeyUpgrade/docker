from django.db import models

from config.settings import AUTH_USER_MODEL


class Courses(models.Model):
    name = models.CharField(
        max_length=35,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Укажите описание курса",
    )

    preview = models.ImageField(
        upload_to="materials/previews_classes",
        blank=True,
        null=True,
        verbose_name="Картинка курса",
        help_text="Картинка курса",
    )

    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lessons(models.Model):
    name = models.CharField(
        max_length=35,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Укажите описание урока",
    )

    preview = models.ImageField(
        upload_to="materials/previews_lessons",
        blank=True,
        null=True,
        verbose_name="Картинка урока",
        help_text="Картинка урока",
    )

    video_url = models.TextField(
        verbose_name="Cсылка на видео",
        help_text="Прикрепите ссылку на видео для урока.",
    )

    courses = models.ForeignKey(
        Courses, on_delete=models.SET_NULL, related_name="lessons", blank=True, null=True
    )

    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name

class Subscription(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='курс')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
