from django import forms

from .models import Student


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

        for field in self.fields.values():

            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control"