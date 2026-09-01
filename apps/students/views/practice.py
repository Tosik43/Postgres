from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ..models.student import Student
from ..forms.practice import PracticeForm
from ..models.practice import Practice
from django.urls import reverse


def practice_create(request, student_pk):

    student = get_object_or_404(
        Student,
        pk=student_pk,
        is_active=True,
    )

    if request.method == "POST":

        form = PracticeForm(request.POST)

        if form.is_valid():

            practice = form.save(commit=False)
            practice.student = student
            practice.save()

            messages.success(
                request,
                "Практика успешно добавлена.",
            )

            return redirect(
                f"{reverse('student_detail', kwargs={'pk': student.pk})}?tab=practice"
            )

    else:

        form = PracticeForm()

    return render(
        request,
        "students/practice/form.html",
        {
            "form": form,
            "practice": None,
            "student": student,
        },
    )

def practice_edit(request, pk):

    practice = get_object_or_404(
        Practice,
        pk=pk,
    )

    student = practice.student

    if request.method == "POST":

        form = PracticeForm(
            request.POST,
            instance=practice,
        )

        if form.is_valid():

            form.save()

            return redirect(
                f"{reverse('student_detail', kwargs={'pk': student.pk})}?tab=practice"
            )

    else:

        form = PracticeForm(
            instance=practice,
        )

    return render(
        request,
        "students/practice/form.html",
        {
            "student": student,
            "practice": practice,
            "form": form,
        },
    )

def practice_delete(request, pk):

    practice = get_object_or_404(
        Practice,
        pk=pk,
    )

    student = practice.student

    if request.method == "POST":

        practice.delete()

        messages.success(
            request,
            "Практика успешно удалена.",
        )

        return redirect(
            f"{reverse('student_detail', kwargs={'pk': student.pk})}?tab=practice"
        )

    return redirect(
        "student_detail",
        pk=student.pk,
    )