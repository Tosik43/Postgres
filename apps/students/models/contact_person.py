from django.db import models

from ..validators import validate_phone


class ContactPerson(models.Model):

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="contact_persons",
        verbose_name="Студент"
    )

    full_name = models.CharField(
        "ФИО",
        max_length=255
    )

    relationship = models.CharField(
        "Родство",
        max_length=100
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

    class Meta:
        verbose_name = "Контактное лицо"
        verbose_name_plural = "Контактные лица"
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} — {self.relationship}"