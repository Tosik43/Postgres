from django import forms

from ..models import DisabilityCertificate


class DisabilityCertificateForm(forms.ModelForm):

    class Meta:
        model = DisabilityCertificate
        fields = [
            "series",
            "number",
            "issue_date",
            "is_permanent",
            "expiry_date",
            "disability_group",
            "disability_reason",
            "establishment_type",
            "disability_start_date",
            "disability_end_date",
            "next_reexamination_date",
            "document",
        ]

        widgets = {
            "series": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "number": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "issue_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "is_permanent": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "expiry_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "disability_group": forms.Select(
                attrs={"class": "form-select"}
            ),
            "disability_reason": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "establishment_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "disability_start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "disability_end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "next_reexamination_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "document": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        is_permanent = cleaned_data.get("is_permanent")
        issue_date = cleaned_data.get("issue_date")
        expiry_date = cleaned_data.get("expiry_date")

        if is_permanent:
            cleaned_data["expiry_date"] = None

        elif not expiry_date:
            self.add_error(
                "expiry_date",
                "Укажите дату окончания или отметьте справку как бессрочную.",
            )

        if issue_date and expiry_date and expiry_date < issue_date:
            self.add_error(
                "expiry_date",
                "Дата окончания не может быть раньше даты выдачи.",
            )

        return cleaned_data
