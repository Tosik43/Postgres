from django import forms
from .models import Student

from .education_history import (
    EducationHistory,
    ChangeReason,
)


class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [
            "full_name",
            "birth_date",
            "gender",
            "snils",
            "email",
            "vk",
            "phone",
            "enrollment_year",
            "graduation_year",
            "study_status",
            "expulsion_reason",
        ]

        widgets = {

            "birth_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "expulsion_reason": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                }
            ),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["birth_date"].input_formats = ["%Y-%m-%d"]

        self.fields["snils"].widget.attrs["placeholder"] = "___-___-___ __"
        self.fields["phone"].widget.attrs["placeholder"] = "+7 (___) ___-__-__"

        self.fields["snils"].widget.attrs.pop("maxlength", None)
        self.fields["phone"].widget.attrs.pop("maxlength", None)

        for field_name, field in self.fields.items():
            css_class = field.widget.attrs.get("class", "form-control")

            if self.is_bound and field_name in self.errors:
                field.widget.attrs["class"] = f"{css_class} is-invalid"
            else:
                field.widget.attrs["class"] = css_class


class EducationHistoryForm(forms.ModelForm):

    class Meta:
        model = EducationHistory

        fields = [
            "faculty",
            "educational_program",
            "enrollment_year",
            "course",
            "semester",
            "study_group",
            "study_form",
            "funding_type",
            "status",
            "start_date",
            "end_date",
            "change_reasons",
        ]

        widgets = {

            "enrollment_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1990,
                }
            ),

            "course": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 10,
                }
            ),

            "semester": forms.Select(
                choices=[
                    (1, "1 семестр"),
                    (2, "2 семестр"),
                ],
                attrs={
                    "class": "form-select",
                }
            ),

            "study_group": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, ИТ-101",
                }
            ),

            "study_form": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "funding_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "start_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "end_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "change_reasons": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": 6,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Даты из HTML input type="date"
        self.fields["start_date"].input_formats = [
            "%Y-%m-%d"
        ]

        self.fields["end_date"].input_formats = [
            "%Y-%m-%d"
        ]

        # Только активные причины
        self.fields["change_reasons"].queryset = (
            ChangeReason.objects
            .filter(is_active=True)
            .order_by("name")
        )

        self.fields["faculty"].queryset = (
            self.fields["faculty"].queryset
            .filter(is_active=True)
            .order_by("name")
        )

        self.fields["educational_program"].queryset = (
            self.fields["educational_program"].queryset
            .filter(is_active=True)
            .order_by("code", "name")
        )

        for field_name, field in self.fields.items():

            css_class = field.widget.attrs.get(
                "class",
                "form-control"
            )

            if self.is_bound and field_name in self.errors:
                field.widget.attrs["class"] = (
                    f"{css_class} is-invalid"
                )
            else:
                field.widget.attrs["class"] = css_class