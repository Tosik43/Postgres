from django import forms

from ..models import ContactPerson


class ContactPersonForm(forms.ModelForm):

    class Meta:
        model = ContactPerson

        fields = [
            "full_name",
            "relationship",
            "phone",
            "email"
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ФИО контактного лица",
                }
            ),

            "relationship": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, мать, отец, опекун",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+7 (___) ___-__-__",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@mail.ru",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["phone"].widget.attrs.pop(
            "maxlength",
            None
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