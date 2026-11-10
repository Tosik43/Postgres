from django.shortcuts import get_object_or_404, redirect, render

from ..models import Student
from ..forms import StudentSpecialNeedsForm


def student_special_needs(request, student_pk):
    student = get_object_or_404(
        Student,
        pk=student_pk,
    )

    special_needs = getattr(
        student,
        "special_needs",
        None,
    )

    if request.method == "POST":
        form = StudentSpecialNeedsForm(
            request.POST,
            instance=special_needs,
        )

        if form.is_valid():
            special_needs = form.save(commit=False)
            special_needs.student = student
            special_needs.save()

            return redirect(
                f"/{student.pk}/?tab=special_needs"
            )

    else:
        form = StudentSpecialNeedsForm(
            instance=special_needs,
        )

    return render(
        request,
        "students/student_special_needs.html",
        {
            "student": student,
            "form": form,
            "special_needs": special_needs,
        },
    )
