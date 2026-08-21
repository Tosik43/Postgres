from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ContactPersonForm
from ..models import Student


def contact_person_create(request, student_pk):

    student = get_object_or_404(
        Student,
        pk=student_pk
    )

    if request.method == "POST":

        form = ContactPersonForm(
            request.POST
        )

        if form.is_valid():

            contact_person = form.save(
                commit=False
            )

            contact_person.student = student
            contact_person.save()

            messages.success(
                request,
                "Контактное лицо успешно добавлено."
            )

            return redirect(
                "student_detail",
                pk=student.pk
            )

    else:

        form = ContactPersonForm()

    return render(
        request,
        "students/contact_person/form.html",
        {
            "form": form,
            "student": student,
        }
    )