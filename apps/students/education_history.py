from django.db import models
from django.core.exceptions import ValidationError


class StudyForm(models.TextChoices):
    FULL_TIME = "full_time", "Очная"
    PART_TIME = "part_time", "Заочная"
    PART_TIME_FULL = "part_time_full", "Очно-заочная"


class FundingType(models.TextChoices):
    BUDGET = "budget", "Бюджет"
    CONTRACT = "contract", "Контракт"


class EducationHistoryStatus(models.TextChoices):
    STUDYING = "studying", "Обучается"
    ACADEMIC_LEAVE = "academic_leave", "Академический отпуск"
    EXPELLED = "expelled", "Отчислен"
    GRADUATED = "graduated", "Выпустился"


class ChangeReason(models.Model):

    name = models.CharField(
        "Причина",
        max_length=100,
        unique=True
    )

    is_active = models.BooleanField(
        "Активна",
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Причина изменения обучения"
        verbose_name_plural = "Причины изменения обучения"
        ordering = ["name"]

    def __str__(self):
        return self.name


class EducationHistory(models.Model):

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="education_history",
        verbose_name="Студент"
    )

    faculty = models.ForeignKey(
        "directories.Faculty",
        on_delete=models.PROTECT,
        related_name="education_history",
        verbose_name="Факультет"
    )

    educational_program = models.ForeignKey(
        "directories.EducationalProgram",
        on_delete=models.PROTECT,
        related_name="education_history",
        verbose_name="Образовательная программа"
    )

    enrollment_year = models.PositiveSmallIntegerField(
        "Год обучения"
    )

    course = models.PositiveSmallIntegerField(
        "Курс"
    )

    semester = models.PositiveSmallIntegerField(
        "Семестр"
    )

    study_group = models.CharField(
        "Учебная группа",
        max_length=50
    )

    study_form = models.CharField(
        "Форма обучения",
        max_length=20,
        choices=StudyForm.choices
    )

    funding_type = models.CharField(
        "Тип финансирования",
        max_length=20,
        choices=FundingType.choices
    )

    status = models.CharField(
        "Статус обучения",
        max_length=20,
        choices=EducationHistoryStatus.choices
    )

    start_date = models.DateField(
        "Начало обучения"
    )

    end_date = models.DateField(
        "Конец обучения",
        null=True,
        blank=True
    )

    change_reasons = models.ManyToManyField(
        ChangeReason,
        blank=True,
        related_name="education_history",
        verbose_name="Причины изменения"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "История обучения"
        verbose_name_plural = "История обучения"

        ordering = [
            "student",
            "start_date",
            "course",
            "semester"
        ]

        indexes = [
            models.Index(
                fields=["student", "start_date"]
            ),
            models.Index(
                fields=["faculty", "start_date"]
            ),
            models.Index(
                fields=["educational_program", "start_date"]
            ),
            models.Index(
                fields=["status"]
            ),
            models.Index(
                fields=["funding_type"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.student} — "
            f"{self.educational_program} — "
            f"{self.course} курс, "
            f"{self.semester} семестр"
        )

    def clean(self):
        super().clean()

        if self.course < 1:
            raise ValidationError({
                "course": "Курс должен быть не меньше 1."
            })

        if self.course > 10:
            raise ValidationError({
                "course": "Некорректный номер курса."
            })

        if self.semester not in (1, 2):
            raise ValidationError({
                "semester": "Семестр должен быть 1 или 2."
            })

        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    "end_date":
                    "Дата окончания не может быть раньше даты начала."
                })

        if (
            self.status in (
                EducationHistoryStatus.GRADUATED,
                EducationHistoryStatus.EXPELLED,
            )
            and not self.end_date
        ):
            raise ValidationError({
                "end_date":
                "Для завершённого периода необходимо указать дату окончания."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)