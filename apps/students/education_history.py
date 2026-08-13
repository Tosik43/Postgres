from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
import re


class StudyForm(models.TextChoices):
    FULL_TIME = "full_time", "Очная"
    PART_TIME = "part_time", "Заочная"
    PART_TIME_FULL = "part_time_full", "Очно-заочная"


class FundingType(models.TextChoices):
    BUDGET = "budget", "Бюджет"
    CONTRACT = "contract", "Контракт"


class EducationHistoryStatus(models.TextChoices):
    STUDYING = "studying", "Обучается"
    TRANSFERRED = "transferred", "Перевелся"
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

    academic_year = models.CharField(
        "Учебный год",
        max_length=9
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
            "academic_year",
            "course",
            "semester",
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
            f"{self.student} - "
            f"{self.educational_program} - "
            f"{self.course} курс, "
            f"{self.semester} семестр"
        )

    def clean(self):
        super().clean()

        current_year = date.today().year

        if not re.match(r"^\d{4}/\d{4}$", self.academic_year):
            raise ValidationError({
                "academic_year":
                "Учебный год должен быть указан в формате 2021/2022."
            })

        start_year, end_year = map(
            int,
            self.academic_year.split("/")
        )

        if end_year != start_year + 1:
            raise ValidationError({
                "academic_year":
                "Учебный год должен состоять из двух последовательных лет."
            })

        if start_year < 1990 or start_year > current_year + 1:
            raise ValidationError({
                "academic_year":
                "Некорректный учебный год."
            })

        academic_year_start = date(
            start_year,
            9,
            1
        )

        academic_year_end = date(
            end_year,
            8,
            31
        )

        if self.start_date:

            if not (
                academic_year_start
                <= self.start_date
                <= academic_year_end
            ):
                raise ValidationError({
                    "start_date":
                    f"Дата начала должна находиться "
                    f"в пределах учебного года {self.academic_year}."
                })

        if self.end_date:

            if not (
                academic_year_start
                <= self.end_date
                <= academic_year_end
            ):
                raise ValidationError({
                    "end_date":
                    f"Дата окончания должна находиться "
                    f"в пределах учебного года {self.academic_year}."
                })

        if self.course < 1:
            raise ValidationError({
                "course":
                "Курс должен быть не меньше 1."
            })

        if self.course > 10:
            raise ValidationError({
                "course":
                "Некорректный номер курса."
            })

        if self.semester not in (1, 2):
            raise ValidationError({
                "semester":
                "Семестр должен быть 1 или 2."
            })

        if self.start_date and self.end_date:

            if self.end_date < self.start_date:
                raise ValidationError({
                    "end_date":
                    "Дата окончания не может быть раньше даты начала."
                })

        if self.start_date and self.student_id:

            overlapping_period = (
                EducationHistory.objects
                .filter(
                    student_id=self.student_id,
                    start_date__lte=(
                        self.end_date
                        if self.end_date
                        else date.max
                    ),
                )
                .exclude(pk=self.pk)
                .filter(
                    models.Q(end_date__isnull=True)
                    | models.Q(
                        end_date__gte=self.start_date
                    )
                )
                .exists()
            )

            if overlapping_period:
                raise ValidationError({
                    "__all__":
                    "Период обучения пересекается с "
                    "другой записью этого студента."
                })

        if (
            self.status in (
                EducationHistoryStatus.TRANSFERRED,
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