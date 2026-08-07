from django.db import models
from .validators import *
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone


class StudyStatus(models.TextChoices):
    STUDYING = "studying", "Обучается"
    EXPELLED = "expelled", "Отчислен"
    GRADUATED = "graduated", "Выпустился"
    ACADEMIC = "academic_leave", "Академический отпуск"


class Gender(models.TextChoices):
    MALE = "M", "Мужской"
    FEMALE = "F", "Женский"


class Student(models.Model):

    full_name = models.CharField("ФИО", max_length=255)

    birth_date = models.DateField("Дата рождения")

    gender = models.CharField(
        "Пол",
        max_length=1,
        choices=Gender.choices
    )

    snils = models.CharField(
    "СНИЛС",
    max_length=14,
    unique=True,
    validators=[validate_snils]
    )

    email = models.EmailField("Email", blank=True)

    vk = models.URLField(
        "VK",
        blank=True
    )

    phone = models.CharField(
    "Телефон",
    max_length=18,
    validators=[validate_phone]
    )

    enrollment_year = models.PositiveSmallIntegerField(
        "Год поступления"
    )

    graduation_year = models.PositiveSmallIntegerField(
        "Год окончания",
        null=True,
        blank=True
    )

    study_status = models.CharField(
    "Статус обучения",
    max_length=20,
    choices=StudyStatus.choices,
    default=StudyStatus.STUDYING
    )

    expulsion_reason = models.TextField(
        "Причина отчисления",
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(
        "Активен",
        default=True
    )

    deleted_at = models.DateTimeField(
        "Дата удаления",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ["full_name"]

        indexes = [
            models.Index(fields=["full_name"]),
            models.Index(fields=["snils"]),
        ]

    def __str__(self):
        return self.full_name

    def clean(self):
        super().clean()

        # Убираем лишние пробелы
        self.full_name = " ".join(self.full_name.split())

        # Каждое слово с большой буквы
        self.full_name = self.full_name.title()

        # Проверка возраста

        today = date.today()

        age = (
            today.year
            - self.birth_date.year
            - (
                (today.month, today.day)
                <
                (self.birth_date.month, self.birth_date.day)
            )
        )

        if age < 14:
            raise ValidationError({
                "birth_date":
                "Возраст студента не может быть меньше 14 лет."
            })

        if (
            self.graduation_year
            and
            self.graduation_year < self.enrollment_year
        ):
            raise ValidationError({
                "graduation_year":
                "Год окончания не может быть меньше года поступления."
            })

        # Проверка дат

        current_year = date.today().year

        if (
            self.enrollment_year < 1990
            or
            self.enrollment_year > current_year + 1
        ):
            raise ValidationError({
                "enrollment_year":
                "Некорректный год поступления."
            })

        if self.graduation_year:

            if self.graduation_year > current_year + 10:

                raise ValidationError({
                    "graduation_year":
                    "Некорректный год окончания."
                })

        if (
            self.study_status == StudyStatus.EXPELLED
            and
            not self.expulsion_reason.strip()
        ):
            raise ValidationError({
                "expulsion_reason": "Укажите причину отчисления."
            })

    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

