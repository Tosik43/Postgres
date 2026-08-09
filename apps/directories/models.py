from django.db import models

class Faculty(models.Model):

    name = models.CharField(
        "Полное название",
        max_length=255,
        unique=True
    )

    abbreviation = models.CharField(
        "Аббревиатура",
        max_length=30,
        unique=True
    )

    is_active = models.BooleanField(
        "Активен",
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    deleted_at = models.DateTimeField(
        "Дата удаления",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"
        ordering = ["name"]

    def __str__(self):
        return f"{self.abbreviation} — {self.name}"

class EducationalProgram(models.Model):

    class EducationLevel(models.TextChoices):
        BACHELOR = "bachelor", "Бакалавриат"
        SPECIALIST = "specialist", "Специалитет"
        MASTER = "master", "Магистратура"
        POSTGRADUATE = "postgraduate", "Аспирантура"

    code = models.CharField(
        "Код направления",
        max_length=20
    )

    name = models.CharField(
        "Название направления",
        max_length=255
    )

    education_level = models.CharField(
        "Уровень образования",
        max_length=20,
        choices=EducationLevel.choices
    )

    is_active = models.BooleanField(
        "Активен",
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    deleted_at = models.DateTimeField(
        "Дата удаления",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"
        ordering = ["code", "name"]

        constraints = [
        models.UniqueConstraint(
            fields=["code", "education_level"],
            name="unique_program_code_and_level"
        )
    ]

    def __str__(self):
        return f"{self.code} — {self.name}"