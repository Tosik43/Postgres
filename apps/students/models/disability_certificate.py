import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

def validate_certificate_file(file):
    max_size = 10 * 1024 * 1024
    allowed_extensions = {".pdf", ".jpg", ".jpeg", ".png"}

    extension = os.path.splitext(file.name)[1].lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            "Допустимые форматы файлов: PDF, JPG, JPEG и PNG."
        )

    if file.size > max_size:
        raise ValidationError(
            "Размер файла не должен превышать 10 МБ."
        )

class DisabilityCertificate(models.Model):

    class DisabilityGroup(models.TextChoices):
        GROUP_I = "I", "I группа"
        GROUP_II = "II", "II группа"
        GROUP_III = "III", "III группа"
        CHILD = "child", "Ребёнок-инвалид"

    class EstablishmentType(models.TextChoices):
        FIRST_TIME = "first_time", "Впервые"
        REPEATED = "repeated", "Повторно"

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="disability_certificates",
        verbose_name="Студент",
    )

    series = models.CharField(
        "Серия справки",
        max_length=50,
        blank=True,
    )

    number = models.CharField(
        "Номер справки",
        max_length=100,
        blank=True,
    )

    issue_date = models.DateField(
        "Дата выдачи",
    )

    is_permanent = models.BooleanField(
        "Бессрочная",
        default=False,
    )

    expiry_date = models.DateField(
        "Дата окончания действия",
        null=True,
        blank=True,
    )

    disability_group = models.CharField(
        "Группа инвалидности",
        max_length=10,
        choices=DisabilityGroup.choices,
        blank=True,
    )

    disability_reason = models.CharField(
        "Причина инвалидности",
        max_length=255,
        blank=True,
    )

    establishment_type = models.CharField(
        "Инвалидность установлена",
        max_length=20,
        choices=EstablishmentType.choices,
        blank=True,
    )

    disability_start_date = models.DateField(
        "Дата установления инвалидности",
        null=True,
        blank=True,
    )

    disability_end_date = models.DateField(
        "Дата окончания инвалидности",
        null=True,
        blank=True,
    )

    next_reexamination_date = models.DateField(
        "Дата следующего переосвидетельствования",
        null=True,
        blank=True,
    )

    document = models.FileField(
        "Файл справки",
        upload_to="disability_certificates/",
        blank=True,
        validators=[validate_certificate_file],
    )

    created_at = models.DateTimeField(
        "Дата внесения в систему",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Справка МСЭ"
        verbose_name_plural = "Справки МСЭ"
        ordering = ["-issue_date", "-created_at"]

    def clean(self):
        super().clean()

        if self.is_permanent:
            self.expiry_date = None
        elif self.expiry_date is None:
            raise ValidationError({
                "expiry_date": (
                    "Укажите дату окончания действия "
                    "или отметьте справку как бессрочную."
                )
            })

        if (
            self.expiry_date is not None
            and self.expiry_date < self.issue_date
        ):
            raise ValidationError({
                "expiry_date": (
                    "Дата окончания действия не может быть "
                    "раньше даты выдачи."
                )
            })

    @property
    def is_active(self):
        today = timezone.localdate()

        if self.is_permanent:
            return True

        return (
            self.issue_date <= today
            and self.expiry_date is not None
            and self.expiry_date >= today
        )

    def __str__(self):
        certificate_number = self.number or "без номера"

        return (
            f"Справка МСЭ {certificate_number} — "
            f"{self.student}"
        )
