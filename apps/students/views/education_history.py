from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from django.contrib import messages
from django.core.exceptions import ValidationError

from ..models import (
    Student,
    EducationHistory,
)

from ..forms import EducationHistoryForm

def education_history_list(request, student_pk):
    student = get_object_or_404(
        Student,
        pk=student_pk
    )

    history = (
        EducationHistory.objects
        .filter(student=student)
        .select_related(
            "faculty",
            "educational_program"
        )
        .prefetch_related("change_reasons")
        .order_by(
            "academic_year",
            "course",
            "semester"
        )
    )

    return render(
        request,
        "students/education_history/list.html",
        {
            "student": student,
            "history": history,
        }
    )


def education_history_create(request, student_pk):
    student = get_object_or_404(
        Student,
        pk=student_pk
    )

    if request.method == "POST":

        form = EducationHistoryForm(
            request.POST
        )

        form.instance.student = student

        if form.is_valid():

            try:
                history = form.save()

            except ValidationError as e:
                form.add_error(None, e)

            else:
                messages.success(
                    request,
                    "Запись истории обучения успешно добавлена."
                )

                return redirect(
                    "education_history_list",
                    student_pk=student.pk
                )

    else:

        form = EducationHistoryForm()

    return render(
        request,
        "students/education_history/form.html",
        {
            "form": form,
            "student": student,
            "history_record": None,
        }
    )

def education_history_edit(request, pk):
    history_record = get_object_or_404(
        EducationHistory,
        pk=pk
    )

    if request.method == "POST":
        form = EducationHistoryForm(
            request.POST,
            instance=history_record
        )

        if form.is_valid():

            try:
                form.save()

            except ValidationError as e:
                form.add_error(None, e)

            else:
                messages.success(
                    request,
                    "Запись истории обучения успешно сохранена."
                )

                return redirect(
                    "education_history_list",
                    student_pk=history_record.student.pk
                )

    else:
        form = EducationHistoryForm(
            instance=history_record
        )

    return render(
        request,
        "students/education_history/form.html",
        {
            "form": form,
            "student": history_record.student,
            "history_record": history_record,
        }
    )


def education_history_delete(request, pk):
    history_record = get_object_or_404(
        EducationHistory,
        pk=pk
    )

    student_pk = history_record.student.pk

    if request.method == "POST":
        history_record.delete()

        messages.success(
            request,
            "Запись истории обучения удалена."
        )

    return redirect(
        "education_history_list",
        student_pk=student_pk
    )