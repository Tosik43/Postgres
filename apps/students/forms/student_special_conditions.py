from django import forms

from ..models import StudentSpecialConditions


class StudentSpecialConditionsForm(forms.ModelForm):

    TECHNICAL_AIDS = [
        (
            "sound_amplification",
            "Звукоусиливающая аппаратура",
        ),
        (
            "multimedia",
            "Мультимедийные средства",
        ),
        (
            "braille_computer",
            "Брайлевская компьютерная техника",
        ),
        (
            "electronic_magnifier",
            "Электронные лупы",
        ),
        (
            "video_magnifier",
            "Видеоувеличители",
        ),
        (
            "reading_machine",
            "Читающие машины",
        ),
        (
            "screen_reader",
            "Программы невизуального доступа к информации",
        ),
        (
            "speech_synthesizer",
            "Программы-синтезаторы речи",
        ),
        (
            "adapted_computer",
            "Компьютерная техника, адаптированная для лиц "
            "с ограниченными двигательными возможностями",
        ),
        (
            "special_software",
            "Специальное программное обеспечение",
        ),
        (
            "alternative_input",
            "Альтернативные устройства ввода информации",
        ),
    ]

    ASSESSMENT_FORMATS = [
        ("oral", "Устно"),
        ("written_paper", "Письменно на бумаге"),
        ("written_computer", "Письменно на компьютере"),
        ("testing", "В форме тестирования"),
    ]

    technical_aids = forms.MultipleChoiceField(
        label="Специальные технические средства обучения",
        choices=TECHNICAL_AIDS,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    assessment_formats = forms.MultipleChoiceField(
        label="Предпочтительные формы контроля успеваемости",
        choices=ASSESSMENT_FORMATS,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = StudentSpecialConditions

        fields = [
            "technical_aids",
            "other_technical_aids",
            "assessment_formats",
            "additional_assessment_time",
            "educational_support",
            "sign_language_interpretation",
            "assistant_support",
            "adapted_physical_education",
            "physical_education_preferences",
            "distance_learning",
            "other_conditions",
            "no_special_conditions_required",
            "adapted_program_informed",
            "adapted_program_need",
            "individual_plan_informed",
            "individual_plan_need",
            "teacher_information_consent",
        ]

        widgets = {
            "other_technical_aids": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "physical_education_preferences": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "other_conditions": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "adapted_program_need": forms.RadioSelect,
            "individual_plan_need": forms.RadioSelect,
            "teacher_information_consent": forms.RadioSelect,
        }

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data.get("adapted_physical_education")
            and not cleaned_data.get(
                "physical_education_preferences", ""
            ).strip()
        ):
            self.add_error(
                "physical_education_preferences",
                "Укажите предпочтения по физической культуре.",
            )

        if cleaned_data.get("no_special_conditions_required"):
            conditions = [
                "technical_aids",
                "other_technical_aids",
                "assessment_formats",
                "additional_assessment_time",
                "educational_support",
                "sign_language_interpretation",
                "assistant_support",
                "adapted_physical_education",
                "distance_learning",
                "other_conditions",
            ]

            if any(cleaned_data.get(field) for field in conditions):
                self.add_error(
                    "no_special_conditions_required",
                    "Нельзя одновременно выбрать специальные условия "
                    "и указать, что они не требуются.",
                )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in (
            "adapted_program_need",
            "individual_plan_need",
            "teacher_information_consent",
        ):
            field = self.fields[field_name]
            field.choices = [
                (value, label)
                for value, label in field.choices
                if value != ""
            ]
