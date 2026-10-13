from django.shortcuts import get_object_or_404, redirect, render

from ..forms import DisabilityCertificateForm
from ..models import Student


def disability_certificate_create(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)

    if request.method == "POST":
        form = DisabilityCertificateForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.student = student
            certificate.save()

            return redirect(f"/{student.pk}/?tab=special_needs")

    else:
        form = DisabilityCertificateForm()

    return render(
        request,
        "students/disability_certificate_form.html",
        {
            "student": student,
            "form": form,
        },
    )

def disability_certificate_history(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)

    disability_certificates = student.disability_certificates.all()

    return render(
        request,
        "students/disability_certificate_history.html",
        {
            "student": student,
            "disability_certificates": disability_certificates,
        },
    )

def disability_certificate_edit(request, student_pk, certificate_pk):
    student = get_object_or_404(Student, pk=student_pk)

    certificate = get_object_or_404(
        student.disability_certificates,
        pk=certificate_pk,
    )

    if request.method == "POST":
        form = DisabilityCertificateForm(
            request.POST,
            request.FILES,
            instance=certificate,
        )

        if form.is_valid():
            form.save()

            return redirect(
                f"/{student.pk}/?tab=disability_certificates"
            )

    else:
        form = DisabilityCertificateForm(instance=certificate)

    return render(
        request,
        "students/disability_certificate_form.html",
        {
            "student": student,
            "form": form,
            "certificate": certificate,
            "is_edit": True,
        },
    )
