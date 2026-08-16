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
        ]

        widgets = {

            "birth_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
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
            "academic_year",
            "course",
            "semester",
            "study_group",
            "study_form",
            "funding_type",
            "status",
            "start_date",
            "end_date",
            "change_reasons",
            "expulsion_reason",
        ]

        widgets = {

            "academic_year": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "2021/2022",
                    "maxlength": 9,
                }
            ),

            "course": forms.Select(
                choices=[
                    (1, "1"),
                    (2, "2"),
                    (3, "3"),
                    (4, "4"),
                    (5, "5"),
                    (6, "6"),
                    (7, "7"),
                    (8, "8"),
                    (9, "9"),
                ],
                attrs={
                    "class": "form-select",
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

            "educational_program": forms.Select(
                attrs={
                    "class": "form-select searchable-program",
                    "data-placeholder": "Начните вводить программу...",
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

            "change_reasons": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "change-reasons-checkboxes",
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

        # Даты из HTML input type="date"
        self.fields["start_date"].input_formats = [
            "%Y-%m-%d"
        ]

        self.fields["end_date"].input_formats = [
            "%Y-%m-%d"
        ]

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

        self.fields["faculty"].empty_label = (
            "Выберите факультет"
        )

        self.fields["educational_program"].empty_label = (
            "Выберите образовательную программу"
        )

        self.fields["study_form"].empty_label = (
            "Выберите форму обучения"
        )

        self.fields["funding_type"].empty_label = (
            "Выберите тип финансирования"
        )

        self.fields["status"].empty_label = (
            "Выберите статус"
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

            self.fields["change_reasons"].required = False