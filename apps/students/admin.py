from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "snils",
    )

    list_filter = (
        "gender",
    )

    search_fields = (
        "full_name",
        "snils",
    )

    ordering = (
        "full_name",
    )