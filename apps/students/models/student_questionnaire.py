from django.db import models


class StudentQuestionnaire(models.Model):

    class PreviousEducationType(models.TextChoices):
        MASS_SCHOOL = "mass_school", "Массовая школа"
        SPECIAL_SCHOOL = (
            "special_school",
            "Специальная (коррекционная) школа",
        )
        HOME_SCHOOL = (
            "home_school",
            "Школа (домашнее обучение)",
        )
        COLLEGE_GENERAL = (
            "college_general",
            "Колледж, техникум (обучение в общей группе)",
        )
        COLLEGE_SPECIAL = (
            "college_special",
            "Колледж, техникум (обучение в отдельной группе, индивидуальное обучение)",
        )
        OTHER = "other", "Другое"

    class AccommodationType(models.TextChoices):
        PARENTS = (
            "parents",
            "С родителями, родственниками",
        )
        DORMITORY = (
            "dormitory",
            "В общежитии вуза",
        )
        RENT = "rent", "Снимать жилье"
        OWN = "own", "В собственном жилье"
        OTHER = "other", "Другое"

    class DecisionTime(models.TextChoices):
        CHILDHOOD = (
            "childhood",
            "Много лет назад, мечта с детства",
        )
        SENIOR_CLASSES = (
            "senior_classes",
            "При обучении в старших классах, при выборе профиля",
        )
        GRADUATION_CLASS = (
            "graduation_class",
            "При обучении в выпускном классе (на последнем курсе)",
        )
        ADMISSION_CAMPAIGN = (
            "admission_campaign",
            "Когда подавал документы в университет, во время приемной кампании",
        )
        OTHER = "other", "Другое"

    class ActivityWay(models.TextChoices):
        SCHOOL_STUDIO = (
            "school_studio",
            "Школа, студия и пр.",
        )
        SELF = "self", "Самостоятельно"

    class ActivityPeriod(models.TextChoices):
        SCHOOL_COLLEGE = (
            "school_college",
            "Во время учебы в школе (колледже)",
        )
        CURRENT = (
            "current",
            "Продолжаю заниматься в настоящее время",
        )

    class PreferredContactMethod(models.TextChoices):
        PHONE = "phone", "Телефон"
        EMAIL = "email", "Электронная почта"
        VK = "vk", "ВКонтакте"
        TELEGRAM = "telegram", "Telegram"
        WHATSAPP = "whatsapp", "WhatsApp"
        VIBER = "viber", "Viber"
        MAX = "max", "МАХ"

    student = models.OneToOneField(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="questionnaire",
        verbose_name="Студент",
    )

    previous_education_type = models.CharField(
        "Предыдущее образование",
        max_length=30,
        choices=PreviousEducationType.choices,
    )

    previous_education_other = models.CharField(
        "Другое (предыдущее образование)",
        max_length=255,
        blank=True,
    )

    accommodation_type = models.CharField(
        "Место проживания в период обучения",
        max_length=20,
        choices=AccommodationType.choices,
    )

    accommodation_other = models.CharField(
        "Другое (место проживания)",
        max_length=255,
        blank=True,
    )

    decision_time = models.CharField(
        "Когда принято решение о поступлении",
        max_length=30,
        choices=DecisionTime.choices,
    )

    decision_time_other = models.CharField(
        "Другое (время принятия решения)",
        max_length=255,
        blank=True,
    )

    choice_arguments = models.JSONField(
        "Аргументы выбора образовательной программы",
        default=list,
    )

    choice_arguments_other = models.CharField(
        "Другое (аргумент выбора)",
        max_length=500,
        blank=True,
    )

    art_types = models.TextField(
        "Виды искусства",
        blank=True,
    )

    art_way = models.CharField(
        "Как занимались искусством",
        max_length=20,
        choices=ActivityWay.choices,
        blank=True,
    )

    art_period = models.CharField(
        "Когда занимались искусством",
        max_length=20,
        choices=ActivityPeriod.choices,
        blank=True,
    )

    art_achievements = models.TextField(
        "Достижения в искусстве",
        blank=True,
    )

    creativity_types = models.TextField(
        "Виды творчества",
        blank=True,
    )

    creativity_way = models.CharField(
        "Как занимались творчеством",
        max_length=20,
        choices=ActivityWay.choices,
        blank=True,
    )

    creativity_period = models.CharField(
        "Когда занимались творчеством",
        max_length=20,
        choices=ActivityPeriod.choices,
        blank=True,
    )

    creativity_achievements = models.TextField(
        "Достижения в творчестве",
        blank=True,
    )

    sport_types = models.TextField(
        "Виды спорта",
        blank=True,
    )

    sport_period = models.CharField(
        "Когда занимались спортом",
        max_length=20,
        choices=ActivityPeriod.choices,
        blank=True,
    )

    sport_achievements = models.TextField(
        "Достижения в спорте",
        blank=True,
    )

    social_activity_types = models.TextField(
        "Виды общественной деятельности",
        blank=True,
    )

    social_activity_period = models.CharField(
        "Когда занимались общественной деятельностью",
        max_length=20,
        choices=ActivityPeriod.choices,
        blank=True,
    )

    abilimpics = models.TextField(
        "Участие в чемпионатах «Абилимпикс»",
        blank=True,
    )

    additional_information = models.TextField(
        "Дополнительные сведения",
        blank=True,
    )

    preferred_contact_methods = models.JSONField(
        "Предпочтительные способы связи",
        default=list,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Анкета студента"
        verbose_name_plural = "Анкеты студентов"

    def __str__(self):
        return f"Анкета — {self.student}"