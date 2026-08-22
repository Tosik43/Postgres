from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ContactPersonForm
from ..models import Student, ContactPerson

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

def contact_person_edit(request, pk):

    contact_person = get_object_or_404(
        ContactPerson,
        pk=pk
    )

    student = contact_person.student

    if request.method == "POST":

        form = ContactPersonForm(
            request.POST,
            instance=contact_person
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Контактное лицо успешно изменено."
            )

            return redirect(
                "student_detail",
                pk=student.pk
            )

    else:

        form = ContactPersonForm(
            instance=contact_person
        )

    return render(
        request,
        "students/contact_person/form.html",
        {
            "form": form,
            "student": student,
            "contact_person": contact_person,
        }
    )

def contact_person_delete(request, pk):

    contact_person = get_object_or_404(
        ContactPerson,
        pk=pk
    )

    student = contact_person.student

    if request.method == "POST":

        name = contact_person.full_name

        contact_person.delete()

        messages.success(
            request,
            f'Контактное лицо "{name}" успешно удалено.'
        )

    return redirect(
        "student_detail",
        pk=student.pk
    )