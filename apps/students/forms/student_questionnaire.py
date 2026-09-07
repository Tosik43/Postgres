from django import forms

from ..models import StudentQuestionnaire


class StudentQuestionnaireForm(forms.ModelForm):

    choice_arguments = forms.MultipleChoiceField(
        label="Три самых важных аргумента выбора образовательной программы",
        choices=[
            (
                "Популярность, престиж профессии",
                "Популярность, престиж профессии",
            ),
            (
                "Доход, который она приносит",
                "Доход, который она приносит",
            ),
            (
                "Карьерные перспективы",
                "Карьерные перспективы",
            ),
            (
                "Легкость поступления",
                "Легкость поступления",
            ),
            (
                "Несложность получения профессии",
                "Несложность получения профессии",
            ),
            (
                "Соответствие семейной традиции",
                "Соответствие семейной традиции",
            ),
            (
                "Соответствие профессии моим увлечениям, хобби",
                "Соответствие профессии моим увлечениям, хобби",
            ),
            (
                "Возможность работы по профессии с учетом состояния моего здоровья",
                "Возможность работы по профессии с учетом состояния моего здоровья",
            ),
            (
                "Другое",
                "Другое",
            ),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    preferred_contact_methods = forms.MultipleChoiceField(
        label="Предпочтительные способы связи",
        choices=StudentQuestionnaire.PreferredContactMethod.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:

        model = StudentQuestionnaire

        fields = [
            "previous_education_type",
            "previous_education_other",
            "accommodation_type",
            "accommodation_other",
            "decision_time",
            "decision_time_other",
            "choice_arguments",
            "choice_arguments_other",
            "art_types",
            "art_way",
            "art_period",
            "art_achievements",
            "creativity_types",
            "creativity_way",
            "creativity_period",
            "creativity_achievements",
            "sport_types",
            "sport_period",
            "sport_achievements",
            "social_activity_types",
            "social_activity_period",
            "abilimpics",
            "additional_information",
            "preferred_contact_methods",
        ]

        widgets = {


            "previous_education_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "previous_education_other": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Укажите свой вариант",
                }
            ),


            "accommodation_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "accommodation_other": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Укажите свой вариант",
                }
            ),


            "decision_time": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "decision_time_other": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Укажите свой вариант",
                }
            ),


            "choice_arguments_other": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Укажите свой вариант",
                }
            ),


            "art_types": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Укажите вид(ы) искусства, которыми занимаетесь (живопись, прикладное искусство, дизайн и пр.) ",
                }
            ),

            "art_way": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "art_period": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "art_achievements": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Укажите достижения (участие в мероприятиях, призовые места, имеющиеся награды, дипломы)",
                }
            ),


            "creativity_types": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Укажите вид(ы) творчества, которыми занимаетесь (музыка, пение, поэзия, танцы, театр, блогерство и пр.)",
                }
            ),

            "creativity_way": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "creativity_period": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "creativity_achievements": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Укажите достижения (участие в мероприятиях, призовые места, имеющиеся награды, дипломы)",
                }
            ),


            "sport_types": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Укажите вид(ы) спорта, которыми занимаетесь",
                }
            ),

            "sport_period": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "sport_achievements": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Укажите достижения (разряд, призовые места, имеющиеся награды)",
                }
            ),


            "social_activity_types": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Укажите виды общественной деятельности, которыми занимаетесь",
                }
            ),

            "social_activity_period": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),


            "abilimpics": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Укажите год, чемпионат, компетенцию и результат",
                }
            ),


            "additional_information": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Дополнительные сведения о себе, хобби, увлечениях",
                }
            ),

        }

        def clean_preferred_contact_methods(self):
            return self.cleaned_data["preferred_contact_methods"]