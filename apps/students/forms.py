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