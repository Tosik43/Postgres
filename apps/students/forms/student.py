from django import forms

from ..models import Student

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
            "health_disorder",
            "health_disorder_comment",
        ]

        widgets = {

            "birth_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "health_disorder": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "health_disorder_comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Дополнительная информация о нарушении здоровья",
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

        self.fields["health_disorder"].queryset = (
            self.fields["health_disorder"].queryset.filter(is_active=True)
            | self.fields["health_disorder"].queryset.filter(
                pk=self.instance.health_disorder_id
            )
            if self.instance.pk and self.instance.health_disorder_id
            else self.fields["health_disorder"].queryset.filter(is_active=True)
        )

        self.fields["health_disorder"].empty_label = "Выберите вид нарушения здоровья"
