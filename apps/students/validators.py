import re
from django.core.exceptions import ValidationError


def validate_snils(value):
    pattern = r'^\d{3}-\d{3}-\d{3} \d{2}$'

    if not re.match(pattern, value):
        raise ValidationError(
            "Введите СНИЛС в формате 123-456-789 00"
        )

def validate_phone(value):
    pattern = r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$'

    if not re.match(pattern, value):
        raise ValidationError(
            "Телефон должен быть в формате +7 (900) 123-45-67"
        )
