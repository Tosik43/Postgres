from django.shortcuts import get_object_or_404, redirect, render

from ..models import Student
from ..forms import StudentSpecialConditionsForm


def student_special_conditions(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)

    special_conditions = getattr(
        student,
        "special_conditions",
        None,
    )

    if request.method == "POST":
        form = StudentSpecialConditionsForm(
            request.POST,
            instance=special_conditions,
        )

        if form.is_valid():
            special_conditions = form.save(commit=False)
            special_conditions.student = student
            special_conditions.save()

            return redirect(
                f"/{student.pk}/?tab=special_conditions"
            )

    else:
        form = StudentSpecialConditionsForm(
            instance=special_conditions,
        )

    return render(
        request,
        "students/student_special_conditions.html",
        {
            "student": student,
            "form": form,
            "special_conditions": special_conditions,
        },
    )
