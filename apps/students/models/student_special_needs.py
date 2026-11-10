from django.db import models


class StudentSpecialNeeds(models.Model):

    class Severity(models.TextChoices):
        NONE = "none", "Нет нарушений"
        MILD = "mild", "Незначительное нарушение"
        SIGNIFICANT = "significant", "Значительное нарушение"
        SEVERE = "severe", "Значительно выраженное нарушение"

    student = models.OneToOneField(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="special_needs",
        verbose_name="Студент",
    )

    has_ipra = models.BooleanField(
        "Предоставлена ИПРА",
        null=True,
        blank=True,
    )

    has_pmpk_conclusion = models.BooleanField(
        "Предоставлено заключение ПМПК",
        null=True,
        blank=True,
    )

    hearing_impairment = models.CharField(
        "Нарушения слуха",
        max_length=20,
        choices=Severity.choices,
        blank=True,
    )

    vision_impairment = models.CharField(
        "Нарушения зрения",
        max_length=20,
        choices=Severity.choices,
        blank=True,
    )

    speech_impairment = models.CharField(
        "Нарушения речи",
        max_length=20,
        choices=Severity.choices,
        blank=True,
    )

    mobility_difficulties = models.CharField(
        "Трудности передвижения",
        max_length=20,
        choices=Severity.choices,
        blank=True,
    )

    organ_system_disorders = models.CharField(
        "Нарушения органов и систем организма",
        max_length=20,
        choices=Severity.choices,
        blank=True,
    )

    other_health_features = models.TextField(
        "Другие особенности здоровья",
        blank=True,
    )

    rehabilitation_aids = models.TextField(
        "Средства коррекции и реабилитации",
        blank=True,
    )

    has_health_episodes = models.BooleanField(
        "Приступы или обмороки, связанные с заболеванием",
        null=True,
        blank=True,
    )

    health_episode_actions = models.TextField(
        "Необходимые действия при приступах",
        blank=True,
    )

    hearing_needs = models.JSONField(
        "Потребности при нарушениях слуха",
        default=list,
    )

    vision_needs = models.JSONField(
        "Потребности при нарушениях зрения",
        default=list,
    )

    preferred_material_formats = models.JSONField(
        "Предпочтительные форматы учебных материалов",
        default=list,
    )

    enlarged_font_size = models.PositiveSmallIntegerField(
        "Размер увеличенного шрифта",
        null=True,
        blank=True,
    )

    speech_needs = models.JSONField(
        "Потребности при нарушениях речи",
        default=list,
    )

    mobility_needs = models.JSONField(
        "Потребности при нарушениях ОДА",
        default=list,
    )

    general_needs = models.JSONField(
        "Общие образовательные потребности",
        default=list,
    )

    other_educational_needs = models.TextField(
        "Другие образовательные потребности",
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Особые образовательные потребности"
        verbose_name_plural = "Особые образовательные потребности"

    def __str__(self):
        return f"Особые образовательные потребности — {self.student}"
