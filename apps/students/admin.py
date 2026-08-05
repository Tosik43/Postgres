from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "snils",
        "study_status",
        "enrollment_year",
    )

    list_filter = (
        "study_status",
        "gender",
        "enrollment_year",
    )

    search_fields = (
        "full_name",
        "snils",
    )

    ordering = (
        "full_name",
    )