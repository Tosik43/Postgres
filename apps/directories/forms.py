from django import forms
from .models import Faculty, EducationalProgram


class FacultyForm(forms.ModelForm):

    class Meta:
        model = Faculty

        fields = [
            "name",
            "abbreviation",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите полное название факультета",
                }
            ),

            "abbreviation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, ВШЭКН",
                }
            ),

        }

class EducationalProgramForm(forms.ModelForm):

    class Meta:
        model = EducationalProgram

        fields = [
            "code",
            "name",
            "education_level",
        ]

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, 09.03.01",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Название направления",
                }
            ),

            "education_level": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }