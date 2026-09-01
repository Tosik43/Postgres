from django import forms

from ..models.practice import Practice


class PracticeForm(forms.ModelForm):

    class Meta:
        model = Practice
        fields = [
            "organization",
            "supervisor",
            "practice_type",
            "semester",
            "referral_source",
            "is_paid",
        ]

        widgets = {
            "student": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "organization": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Название организации",
                }
            ),
            "supervisor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ФИО руководителя",
                }
            ),
            "practice_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "semester": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 12,
                    "placeholder": "Номер семестра",
                }
            ),
            "referral_source": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "is_paid": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_organization(self):
        organization = " ".join(
            self.cleaned_data["organization"].split()
        )

        if len(organization) < 2:
            raise forms.ValidationError(
                "Название организации должно содержать минимум 2 символа."
            )

        return organization

    def clean_supervisor(self):
        supervisor = " ".join(
            self.cleaned_data["supervisor"].split()
        )

        if len(supervisor) < 2:
            raise forms.ValidationError(
                "ФИО руководителя должно содержать минимум 2 символа."
            )

        return supervisor

    def clean_semester(self):
        semester = self.cleaned_data["semester"]

        if not 1 <= semester <= 12:
            raise forms.ValidationError(
                "Номер семестра должен быть от 1 до 12."
            )

        return semester