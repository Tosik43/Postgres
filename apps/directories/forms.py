from django import forms
from .models import Faculty, EducationalProgram, HealthDisorder


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            css_class = field.widget.attrs.get("class", "form-control")
            
            if self.is_bound and field_name in self.errors:
                field.widget.attrs["class"] = f"{css_class} is-invalid"
            else:
                field.widget.attrs["class"] = css_class

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if len(name) > 255:
                raise forms.ValidationError("Название не может быть длиннее 255 символов.")
        return name

    def clean_abbreviation(self):
        abbreviation = self.cleaned_data.get('abbreviation')
        if abbreviation:
            if len(abbreviation) > 30:
                raise forms.ValidationError("Аббревиатура не может быть длиннее 30 символов.")
        return abbreviation

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            css_class = field.widget.attrs.get("class", "form-control")
            
            if self.is_bound and field_name in self.errors:
                field.widget.attrs["class"] = f"{css_class} is-invalid"
            else:
                field.widget.attrs["class"] = css_class

class HealthDisorderForm(forms.ModelForm):

    class Meta:
        model = HealthDisorder

        fields = [
            "name",
            "health_features",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, нарушение слуха",
                }
            ),

            "health_features": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Опишите особенности здоровья",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            css_class = field.widget.attrs.get(
                "class",
                "form-control"
            )

            if (
                self.is_bound
                and field_name in self.errors
            ):
                field.widget.attrs["class"] = (
                    f"{css_class} is-invalid"
                )
            else:
                field.widget.attrs["class"] = css_class

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if name:
            if len(name) > 255:
                raise forms.ValidationError(
                    "Название нарушения не может быть длиннее 255 символов."
                )

        return name