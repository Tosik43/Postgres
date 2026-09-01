from django.db import models
from django.core.exceptions import ValidationError


class Practice(models.Model):

    class PracticeType(models.TextChoices):
        EDUCATIONAL = "educational", "Учебная"
        INDUSTRIAL = "industrial", "Производственная"
        RESEARCH = "research", "Научно-исследовательская"
        PREGRADUATE = "pregraduate", "Преддипломная"

    class ReferralSource(models.TextChoices):
        UNIVERSITY = "university", "Университет"
        STUDENT = "student", "Сам студент"
        ORGANIZATION = "organization", "Организация"
        CAREER_CENTER = "career_center", "Центр карьеры"
        OTHER = "other", "Другое"

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="practices",
        verbose_name="Студент",
    )

    organization = models.CharField(
        "Организация",
        max_length=255,
    )

    supervisor = models.CharField(
        "Руководитель",
        max_length=255,
    )

    practice_type = models.CharField(
        "Вид практики",
        max_length=20,
        choices=PracticeType.choices,
    )

    semester = models.PositiveSmallIntegerField(
        "Семестр",
    )

    referral_source = models.CharField(
        "Кто направил",
        max_length=30,
        choices=ReferralSource.choices,
    )

    is_paid = models.BooleanField(
        "Оплачивается",
        default=False,
    )

    class Meta:
        verbose_name = "Практика"
        verbose_name_plural = "Практики"
        ordering = ["semester", "organization"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "practice_type",
                    "semester",
                ],
                name="unique_student_practice_type_semester",
            ),
        ]

        indexes = [
            models.Index(fields=["student"]),
            models.Index(fields=["organization"]),
            models.Index(fields=["semester"]),
        ]

    def __str__(self):
        return (
            f"{self.organization} — "
            f"{self.get_practice_type_display()}"
        )

    def clean(self):
        super().clean()

        # Убираем лишние пробелы
        self.organization = " ".join(
            self.organization.split()
        )

        self.supervisor = " ".join(
            self.supervisor.split()
        )

        # Проверка организации
        if len(self.organization) < 2:
            raise ValidationError({
                "organization":
                    "Название организации должно содержать минимум 2 символа."
            })

        # Проверка руководителя
        if len(self.supervisor) < 2:
            raise ValidationError({
                "supervisor":
                    "ФИО руководителя должно содержать минимум 2 символа."
            })

        # Проверка семестра
        if not 1 <= self.semester <= 12:
            raise ValidationError({
                "semester":
                    "Номер семестра должен быть от 1 до 12."
            })

        # Проверка вида практики
        valid_practice_types = {
            value
            for value, label in self.PracticeType.choices
        }

        if self.practice_type not in valid_practice_types:
            raise ValidationError({
                "practice_type":
                    "Выбран недопустимый вид практики."
            })

        # Проверка источника направления
        valid_referral_sources = {
            value
            for value, label in self.ReferralSource.choices
        }

        if self.referral_source not in valid_referral_sources:
            raise ValidationError({
                "referral_source":
                    "Выбран недопустимый источник направления."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)