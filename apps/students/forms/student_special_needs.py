from django import forms

from ..models import StudentSpecialNeeds


class StudentSpecialNeedsForm(forms.ModelForm):

    HEARING_CHOICES = [
        ("none", "Нет нарушений слуха"),
        (
            "mild",
            "Незначительное нарушение слуха, не требующее создания специальных условий",
        ),
        (
            "significant",
            "Значительное нарушение слуха – значительное снижение слуховой функции, "
            "доступно восприятие устной речи, но на расстоянии не более чем "
            "2-3 метра от говорящего",
        ),
        (
            "severe",
            "Значительно выраженное нарушение слуха – разборчивое восприятие речи "
            "затруднено / частично считываю информацию с губ говорящего / "
            "только с использованием русского жестового языка",
        ),
    ]

    VISION_CHOICES = [
        ("none", "Нет нарушений зрения"),
        (
            "mild",
            "Незначительное нарушение зрения, не требующее создания специальных условий",
        ),
        (
            "significant",
            "Значительное нарушение зрения – значительное снижение зрительной "
            "функции, но со способностью к восприятию зрительных образов, "
            "печатного материала",
        ),
        (
            "severe",
            "Значительно выраженное нарушение зрения – отсутствие способности "
            "к восприятию зрительных образов, печатного материала",
        ),
    ]

    SPEECH_CHOICES = [
        ("none", "Нет нарушений речи"),
        (
            "mild",
            "Незначительное нарушение речи, которая доступна для понимания "
            "окружающими людьми",
        ),
        (
            "significant",
            "Значительное нарушение речи – искаженная и замедленная речь, "
            "не всегда доступная для понимания окружающими людьми",
        ),
        (
            "severe",
            "Значительно выраженное нарушение речи – отсутствие речи или речь "
            "не понятна для окружающих",
        ),
    ]

    MOBILITY_CHOICES = [
        ("none", "Нет трудностей передвижения"),
        (
            "mild",
            "Незначительные трудности передвижения – передвигаюсь самостоятельно",
        ),
        (
            "significant",
            "Значительные трудности передвижения – передвигаюсь самостоятельно "
            "с помощью опорных средств",
        ),
        (
            "severe",
            "Отсутствие способности передвигаться самостоятельно – передвигаюсь "
            "самостоятельно с собакой-проводником / с сопровождающим / "
            "на кресло-коляске / лежачий",
        ),
    ]

    ORGAN_CHOICES = [
        ("none", "Нет нарушений органов и систем организма"),
        (
            "mild",
            "Наличие хронических заболеваний легкой степени, не требующих "
            "создания каких-либо специальных условий обучения",
        ),
        (
            "significant",
            "Наличие хронических заболеваний средней степени, требующих учета "
            "при организации образовательного процесса",
        ),
        (
            "severe",
            "Наличие хронических заболеваний тяжелой степени, затрудняющих "
            "нормальное протекание образовательного процесса без создания "
            "специальных условий обучения",
        ),
    ]

    HEARING_NEEDS = [
        (
            "visual_materials",
            "Использование наглядных средств обучения, иллюстративного материала, презентаций",
        ),
        (
            "written_tasks",
            "Выполнение заданий преимущественно в письменной форме (на компьютере, на бумаге)",
        ),
        ("clear_speech", "Громкая и четкая речь преподавателя"),
        ("sign_language", "Перевод на русский жестовый язык"),
        (
            "front_row",
            "Выделение рабочего места в первом ряду учебной аудитории",
        ),
    ]

    VISION_NEEDS = [
        (
            "large_font",
            "Представление учебного материала в печатной форме увеличенным шрифтом",
        ),
        (
            "front_row",
            "Выделение рабочего места в первом ряду учебной аудитории",
        ),
        ("large_monitor", "Большой монитор для работы на компьютере"),
        (
            "oral_tasks",
            "Выполнение заданий преимущественно в устной форме",
        ),
        (
            "slide_narration",
            "Речевое сопровождение содержания слайдов презентации, записей на доске",
        ),
        (
            "audio_recording",
            "Использование на лекциях диктофона или других записывающих устройств",
        ),
        (
            "mobile_notes",
            "Использование на занятиях ноутбука или мобильного устройства для записи конспекта",
        ),
    ]

    MATERIAL_FORMATS = [
        ("audio", "В аудио форме (устно)"),
        ("printed", "В печатной форме"),
        ("braille", "В печатной форме шрифтом Брайля"),
        ("electronic", "В электронной форме"),
    ]

    SPEECH_NEEDS = [
        ("extra_oral_time", "Увеличение времени для устного ответа"),
        (
            "written_tasks",
            "Выполнение заданий в письменной форме (на компьютере, на бумаге)",
        ),
    ]

    MOBILITY_NEEDS = [
        (
            "audio_recording",
            "Использование на лекциях диктофона или других записывающих устройств",
        ),
        (
            "mobile_notes",
            "Использование на занятиях ноутбука или мобильного устройства для записи конспекта",
        ),
        (
            "computer_tasks",
            "Выполнение заданий на компьютере (мобильном устройстве)",
        ),
    ]

    GENERAL_NEEDS = [
        (
            "breaks",
            "Необходимость перерывов для отдыха, приема пищи, лекарств и т.п.",
        ),
        (
            "extra_time",
            "Медленный темп работы, требующий дополнительного времени при подготовке ответов и выполнения заданий",
        ),
        (
            "individual_work",
            "Предпочтение индивидуальным формам работы вместо коллективных",
        ),
    ]

    YES_NO_CHOICES = [
        (True, "Да"),
        (False, "Нет"),
    ]

    hearing_impairment = forms.ChoiceField(
        label="Нарушения слуха",
        choices=HEARING_CHOICES,
        initial="none",
        required=True,
        widget=forms.RadioSelect,
    )

    vision_impairment = forms.ChoiceField(
        label="Нарушения зрения",
        choices=VISION_CHOICES,
        initial="none",
        required=True,
        widget=forms.RadioSelect,
    )

    speech_impairment = forms.ChoiceField(
        label="Нарушения речи",
        choices=SPEECH_CHOICES,
        initial="none",
        required=True,
        widget=forms.RadioSelect,
    )

    mobility_difficulties = forms.ChoiceField(
        label="Трудности передвижения",
        choices=MOBILITY_CHOICES,
        initial="none",
        required=True,
        widget=forms.RadioSelect,
    )

    organ_system_disorders = forms.ChoiceField(
        label="Нарушения органов и систем организма",
        choices=ORGAN_CHOICES,
        initial="none",
        required=True,
        widget=forms.RadioSelect,
    )

    has_ipra = forms.TypedChoiceField(
        label="Предоставляю ИПРА",
        choices=[("", "Не указано"), *YES_NO_CHOICES],
        coerce=lambda value: (
            None if value == "" else str(value) == "True"
        ),
        empty_value=None,
        required=False,
        widget=forms.RadioSelect,
    )

    has_pmpk_conclusion = forms.TypedChoiceField(
        label="Предоставляю заключение ПМПК",
        choices=[("", "Не указано"), *YES_NO_CHOICES],
        coerce=lambda value: (
            None if value == "" else str(value) == "True"
        ),
        empty_value=None,
        required=False,
        widget=forms.RadioSelect,
    )

    has_health_episodes = forms.TypedChoiceField(
        label="Приступы или обмороки, связанные с заболеванием",
        choices=[("", "Не указано"), *YES_NO_CHOICES],
        coerce=lambda value: (
            None if value == "" else str(value) == "True"
        ),
        empty_value=None,
        required=False,
        widget=forms.RadioSelect,
    )

    hearing_needs = forms.MultipleChoiceField(
        label="Потребности при нарушениях слуха",
        choices=HEARING_NEEDS,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    vision_needs = forms.MultipleChoiceField(
        label="Потребности при нарушениях зрения",
        choices=VISION_NEEDS,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    preferred_material_formats = forms.MultipleChoiceField(
        label="Предпочтительные форматы учебных материалов",
        choices=MATERIAL_FORMATS,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    speech_needs = forms.MultipleChoiceField(
        label="Потребности при нарушениях речи",
        choices=SPEECH_NEEDS,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    mobility_needs = forms.MultipleChoiceField(
        label="Потребности при нарушениях опорно-двигательного аппарата",
        choices=MOBILITY_NEEDS,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    general_needs = forms.MultipleChoiceField(
        label="Общие образовательные потребности",
        choices=GENERAL_NEEDS,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = StudentSpecialNeeds

        fields = [
            "has_ipra",
            "has_pmpk_conclusion",
            "hearing_impairment",
            "vision_impairment",
            "speech_impairment",
            "mobility_difficulties",
            "organ_system_disorders",
            "other_health_features",
            "rehabilitation_aids",
            "has_health_episodes",
            "health_episode_actions",
            "hearing_needs",
            "vision_needs",
            "preferred_material_formats",
            "enlarged_font_size",
            "speech_needs",
            "mobility_needs",
            "general_needs",
            "other_educational_needs",
        ]

        widgets = {
            "other_health_features": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "rehabilitation_aids": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "health_episode_actions": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "enlarged_font_size": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "other_educational_needs": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data.get("has_health_episodes") is True
            and not cleaned_data.get("health_episode_actions", "").strip()
        ):
            self.add_error(
                "health_episode_actions",
                "Укажите необходимые действия при приступах или обмороках.",
            )

        if (
            cleaned_data.get("enlarged_font_size") is not None
            and "large_font" not in cleaned_data.get("vision_needs", [])
        ):
            self.add_error(
                "enlarged_font_size",
                "Укажите потребность в увеличенном шрифте.",
            )

        return cleaned_data
