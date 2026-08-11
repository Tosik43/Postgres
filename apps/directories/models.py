from django.db import models
from django.core.exceptions import ValidationError


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

    def clean(self):
        super().clean()
        
        self.abbreviation = " ".join(self.abbreviation.split())
        
        self.abbreviation = self.abbreviation.upper()
        
        if len(self.name) < 3:
            raise ValidationError({
                "name": "Название факультета должно содержать минимум 3 символа."
            })
        
        if len(self.abbreviation) < 2:
            raise ValidationError({
                "abbreviation": "Аббревиатура должна содержать минимум 2 символа."
            })
        
        import re
        if not re.match(r'^[A-ZА-Я0-9.]+$', self.abbreviation):
            raise ValidationError({
                "abbreviation": "Аббревиатура может содержать только буквы, цифры и точки."
            })
        
        if Faculty.objects.filter(
            name=self.name
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                "name": f"Факультет с названием '{self.name}' уже существует."
            })
        
        if Faculty.objects.filter(
            abbreviation=self.abbreviation
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                "abbreviation": f"Факультет с аббревиатурой '{self.abbreviation}' уже существует."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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

    def clean(self):
        super().clean()
        
        self.code = " ".join(self.code.split())
        self.name = " ".join(self.name.split())
        
        self.code = self.code.upper()
        
        if len(self.code) < 3:
            raise ValidationError({
                "code": "Код направления должен содержать минимум 3 символа."
            })
        
        import re
        if not re.match(r'^[0-9.]+$', self.code):
            raise ValidationError({
                "code": "Код может содержать только цифры и точки."
            })
        
        if len(self.name) < 3:
            raise ValidationError({
                "name": "Название должно содержать минимум 3 символа."
            })
        
        if EducationalProgram.objects.filter(
            code=self.code,
            education_level=self.education_level
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                "code": f"Программа с кодом '{self.code}' и уровнем '{self.get_education_level_display()}' уже существует."
            })

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)