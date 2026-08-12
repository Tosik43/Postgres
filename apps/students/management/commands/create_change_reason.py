from django.core.management.base import BaseCommand

from apps.students.education_history import ChangeReason


class Command(BaseCommand):

    help = "Создаёт стандартные причины изменения истории обучения"

    reasons = [
        "Перевод на другую образовательную программу",
        "Перевод на другой факультет",
        "Перевод с бюджета на контракт",
        "Перевод с контракта на бюджет",
        "Изменение формы обучения",
        "Изменение учебной группы",
        "Академический отпуск",
        "Выход из академического отпуска",
        "Восстановление после отчисления",
        "Отчисление",
        "Выпуск",
        "Изменение курса",
        "Другое",
    ]

    def handle(self, *args, **options):

        created_count = 0

        for reason in self.reasons:

            _, created = ChangeReason.objects.get_or_create(
                name=reason
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово. Создано новых причин: {created_count}"
            )
        )