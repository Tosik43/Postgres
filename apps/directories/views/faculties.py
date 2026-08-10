from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..forms import FacultyForm
from ..models import Faculty


def faculty_list(request):
    faculties = (
        Faculty.objects
        .filter(is_active=True)
        .order_by("name")
    )

    return render(
        request,
        "directories/faculties/list.html",
        {
            "faculties": faculties,
        },
    )


def faculty_create(request):
    if request.method == "POST":
        form = FacultyForm(request.POST)

        if form.is_valid():
            faculty = form.save()

            messages.success(
                request,
                f'Факультет "{faculty.name}" успешно добавлен.',
            )

            return redirect("faculty_list")

    else:
        form = FacultyForm()

    return render(
        request,
        "directories/faculties/form.html",
        {
            "form": form,
            "faculty": None,
        },
    )


def faculty_edit(request, pk):
    faculty = get_object_or_404(
        Faculty,
        pk=pk,
        is_active=True,
    )

    if request.method == "POST":
        form = FacultyForm(
            request.POST,
            instance=faculty,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Данные факультета успешно сохранены.",
            )

            return redirect("faculty_list")

    else:
        form = FacultyForm(instance=faculty)

    return render(
        request,
        "directories/faculties/form.html",
        {
            "form": form,
            "faculty": faculty,
        },
    )


def faculty_delete(request, pk):
    if request.method != "POST":
        return redirect("faculty_list")

    faculty = get_object_or_404(
        Faculty,
        pk=pk,
        is_active=True,
    )

    faculty.is_active = False
    faculty.deleted_at = timezone.now()
    faculty.save(
        update_fields=["is_active", "deleted_at", "updated_at"]
    )

    messages.success(
        request,
        f'Факультет "{faculty.abbreviation}" успешно удален.',
    )

    return redirect("faculty_list")


def faculty_archive(request):
    faculties = (
        Faculty.objects
        .filter(is_active=False)
        .order_by("-deleted_at")
    )

    return render(
        request,
        "directories/faculties/archive.html",
        {
            "faculties": faculties,
        },
    )


def faculty_restore(request, pk):
    if request.method != "POST":
        return redirect("faculty_archive")

    faculty = get_object_or_404(
        Faculty,
        pk=pk,
        is_active=False,
    )

    faculty.is_active = True
    faculty.deleted_at = None
    faculty.save(
        update_fields=["is_active", "deleted_at", "updated_at"]
    )

    messages.success(
        request,
        "Факультет успешно восстановлен.",
    )

    return redirect("faculty_archive")


def faculty_delete_forever(request, pk):
    if request.method != "POST":
        return redirect("faculty_archive")

    faculty = get_object_or_404(
        Faculty,
        pk=pk,
        is_active=False,
    )

    name = faculty.abbreviation
    faculty.delete()

    messages.success(
        request,
        f'Факультет "{name}" окончательно удален из базы данных.',
    )

    return redirect("faculty_archive")