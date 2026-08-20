from django.db import models
from .validators import *
from django.core.exceptions import ValidationError
from datetime import date

from .education_history import (
    StudyForm,
    FundingType,
    EducationHistoryStatus,
    ChangeReason,
    EducationHistory,
)

from .contact_person import  ContactPerson 


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

        if self.birth_date:  
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
        else:
            raise ValidationError({
                "birth_date": "Дата рождения обязательна для заполнения."
            })
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

