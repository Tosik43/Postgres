from django.db import models


class StudentSpecialConditions(models.Model):

    class NeedChoice(models.TextChoices):
        NOT_NEEDED = "not_needed", "Не нуждаюсь"
        NEEDED = "needed", "Нуждаюсь"

    class ConsentChoice(models.TextChoices):
        AGREE = "agree", "Согласен"
        DISAGREE = "disagree", "Не согласен"

    student = models.OneToOneField(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="special_conditions",
        verbose_name="Студент",
    )

    technical_aids = models.JSONField(
        "Специальные технические средства обучения",
        default=list,
    )

    other_technical_aids = models.TextField(
        "Другие технические средства",
        blank=True,
    )

    assessment_formats = models.JSONField(
        "Предпочтительные формы контроля успеваемости",
        default=list,
    )

    additional_assessment_time = models.BooleanField(
        "Дополнительное время при аттестации",
        default=False,
    )

    educational_support = models.BooleanField(
        "Сопровождение образовательного процесса",
        default=False,
    )

    sign_language_interpretation = models.BooleanField(
        "Услуги перевода на русский жестовый язык",
        default=False,
    )

    assistant_support = models.BooleanField(
        "Помощь ассистента или волонтёра",
        default=False,
    )

    adapted_physical_education = models.BooleanField(
        "Особый порядок освоения физической культуры",
        default=False,
    )

    physical_education_preferences = models.TextField(
        "Предпочтения по физической культуре",
        blank=True,
    )

    distance_learning = models.BooleanField(
        "Использование дистанционных образовательных технологий",
        default=False,
    )

    other_conditions = models.TextField(
        "Другие специальные условия",
        blank=True,
    )

    no_special_conditions_required = models.BooleanField(
        "Специальные условия не требуются",
        default=False,
    )

    adapted_program_informed = models.BooleanField(
        "Ознакомлен с возможностью обучения по адаптированной программе",
        default=False,
    )

    adapted_program_need = models.CharField(
        "Потребность в адаптированной образовательной программе",
        max_length=20,
        choices=NeedChoice.choices,
        blank=True,
    )

    individual_plan_informed = models.BooleanField(
        "Ознакомлен с возможностью обучения по индивидуальному учебному плану",
        default=False,
    )

    individual_plan_need = models.CharField(
        "Потребность в индивидуальном учебном плане",
        max_length=20,
        choices=NeedChoice.choices,
        blank=True,
    )

    teacher_information_consent = models.CharField(
        "Согласие на передачу сведений преподавателям",
        max_length=20,
        choices=ConsentChoice.choices,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Специальные условия обучения"
        verbose_name_plural = "Специальные условия обучения"

    def __str__(self):
        return f"Специальные условия обучения — {self.student}"
