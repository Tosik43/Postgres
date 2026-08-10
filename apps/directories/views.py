from django.shortcuts import get_object_or_404, redirect, render
from .models import Faculty
from .forms import FacultyForm
from django.contrib import messages
from django.utils import timezone


def reference_list(request):

    return render(
        request,
        "directories/reference_list.html"
    )

def faculty_list(request):

    faculties = Faculty.objects.filter(
        is_active=True
    )

    return render(
        request,
        "directories/faculty_list.html",
        {
            "faculties": faculties,
        }
    )

def faculty_create(request):

    if request.method == "POST":

        form = FacultyForm(request.POST)

        if form.is_valid():

            faculty = form.save()

            messages.success(
                request,
                f'Факультет "{faculty.name}" успешно добавлен.'
            )

            return redirect("faculty_list")

    else:

        form = FacultyForm()

    return render(
        request,
        "directories/faculty_form.html",
        {
            "form": form,
        }
    )

def faculty_edit(request, pk):

    faculty = get_object_or_404(
        Faculty,
        pk=pk,
        is_active=True
    )

    if request.method == "POST":

        form = FacultyForm(
            request.POST,
            instance=faculty
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Данные факультета успешно сохранены."
            )

            return redirect("faculty_list")

    else:

        form = FacultyForm(
            instance=faculty
        )

    return render(
        request,
        "directories/faculty_form.html",
        {
            "form": form,
            "faculty": faculty,
        }
    )

def faculty_delete(request, pk):

    faculty = get_object_or_404(
        Faculty,
        pk=pk,
        is_active=True
    )

    if request.method == "POST":

        faculty.is_active = False
        faculty.deleted_at = timezone.now()
        faculty.save()

        messages.success(
            request,
            f'Факультет "{faculty.abbreviation}" успешно удален.'
        )

    return redirect("faculty_list")

def faculty_archive(request):

    faculties = Faculty.objects.filter(
        is_active=False
    ).order_by("-deleted_at")

    return render(
        request,
        "directories/faculty_archive.html",
        {
            "faculties": faculties
        }
    )


def faculty_restore(request, pk):

    if request.method != "POST":
        return redirect("faculty_archive")

    faculty = get_object_or_404(
        Faculty,
        pk=pk,
        is_active=False
    )

    faculty.is_active = True
    faculty.deleted_at = None
    faculty.save()

    messages.success(
        request,
        "Факультет успешно восстановлен."
    )

    return redirect("faculty_archive")

def faculty_delete_forever(request, pk):

    if request.method != "POST":
        return redirect("faculty_archive")

    faculty = get_object_or_404(
        Faculty,
        pk=pk,
        is_active=False
    )

    name = faculty.abbreviation

    faculty.delete()

    messages.success(
        request,
        f'Факультет "{name}" окончательно удален из базы данных.'
    )

    return redirect("faculty_archive")