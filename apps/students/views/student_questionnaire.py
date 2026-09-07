from django.shortcuts import get_object_or_404, redirect, render

from ..models import Student, StudentQuestionnaire
from ..forms import StudentQuestionnaireForm


def student_questionnaire(request, student_pk):

    student = get_object_or_404(
        Student,
        pk=student_pk,
    )

    questionnaire = getattr(
        student,
        "questionnaire",
        None,
    )

    if request.method == "POST":

        form = StudentQuestionnaireForm(
            request.POST,
            instance=questionnaire,
        )

        if form.is_valid():

            questionnaire = form.save(
                commit=False
            )

            questionnaire.student = student

            questionnaire.save()

            return redirect(
            f"/{student.pk}/?tab=profile"
        )

    else:

        form = StudentQuestionnaireForm(
            instance=questionnaire,
        )

    return render(
        request,
        "students/student_questionnaire.html",
        {
            "student": student,
            "form": form,
            "questionnaire": questionnaire,
        },
    )