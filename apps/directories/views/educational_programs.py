from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

from ..models import EducationalProgram
from ..forms import EducationalProgramForm

def educational_program_list(request):

    query = request.GET.get("q", "").strip()
    education_level = request.GET.get("education_level", "")
    sort = request.GET.get("sort", "")
    direction = request.GET.get("direction", "asc")

    programs = EducationalProgram.objects.filter(
        is_active=True
    )

    # Поиск по коду или названию
    if query:
        programs = programs.filter(
            Q(code__icontains=query) |
            Q(name__icontains=query)
        )

    # Фильтр по уровню образования
    if education_level:
        programs = programs.filter(
            education_level=education_level
        )

    # Разрешённые поля сортировки
    allowed_sort_fields = {
        "code": "code",
        "name": "name",
        "education_level": "education_level",
    }

    sort_field = allowed_sort_fields.get(sort)

    if sort_field:

        if direction == "desc":

            programs = programs.order_by(
                f"-{sort_field}"
            )

        else:

            programs = programs.order_by(
                sort_field
            )

    else:

        programs = programs.order_by(
            "code",
            "name"
        )

    context = {
        "programs": programs,
        "query": query,
        "education_level": education_level,
        "education_level_choices": (
            EducationalProgram.EducationLevel.choices
        ),
        "sort": sort,
        "direction": direction,
    }

    # AJAX-запрос
    if request.headers.get(
        "X-Requested-With"
    ) == "XMLHttpRequest":

        tbody = render_to_string(
            "directories/educational_programs/partials/program_table_body.html",
            {
                "programs": programs,
            },
            request=request,
        )

        thead = render_to_string(
            "directories/educational_programs/program_table_head.html",
            {
                "query": query,
                "education_level": education_level,
                "sort": sort,
                "direction": direction,
            },
            request=request,
        )

        return JsonResponse({
            "tbody": tbody,
            "thead": thead,
            "url": request.get_full_path(),
        })

    # Обычный запрос
    return render(
        request,
        "directories/educational_programs/list.html",
        context
    )

def educational_program_create(request):
    if request.method == "POST":
        form = EducationalProgramForm(request.POST)

        if form.is_valid():
            program = form.save()

            messages.success(
                request,
                f'Образовательная программа "{program.code} - '
                f'{program.name}" успешно добавлена.'
            )

            return redirect("educational_program_list")

    else:
        form = EducationalProgramForm()

    return render(
        request,
        "directories/educational_programs/form.html",
        {
            "form": form,
            "program": None,
        }
    )

def educational_program_edit(request, pk):
    program = get_object_or_404(
        EducationalProgram,
        pk=pk,
        is_active=True
    )

    if request.method == "POST":
        form = EducationalProgramForm(
            request.POST,
            instance=program
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Образовательная программа успешно сохранена."
            )

            return redirect("educational_program_list")

    else:
        form = EducationalProgramForm(
            instance=program
        )

    return render(
        request,
        "directories/educational_programs/form.html",
        {
            "form": form,
            "program": program,
        }
    )

def educational_program_delete(request, pk):
    program = get_object_or_404(
        EducationalProgram,
        pk=pk,
        is_active=True
    )

    if request.method == "POST":
        program.is_active = False
        program.deleted_at = timezone.now()
        program.save()

        messages.success(
            request,
            f'Образовательная программа "{program.code}" '
            f'успешно удалена.'
        )

    return redirect("educational_program_list")

def educational_program_archive(request):
    programs = (
        EducationalProgram.objects
        .filter(is_active=False)
        .order_by("-deleted_at")
    )

    return render(
        request,
        "directories/educational_programs/archive.html",
        {
            "programs": programs,
        }
    )

def educational_program_restore(request, pk):
    if request.method != "POST":
        return redirect("educational_program_archive")

    program = get_object_or_404(
        EducationalProgram,
        pk=pk,
        is_active=False
    )

    program.is_active = True
    program.deleted_at = None
    program.save()

    messages.success(
        request,
        "Образовательная программа успешно восстановлена."
    )

    return redirect("educational_program_archive")

def educational_program_delete_forever(request, pk):
    if request.method != "POST":
        return redirect("educational_program_archive")

    program = get_object_or_404(
        EducationalProgram,
        pk=pk,
        is_active=False
    )

    name = f"{program.code} - {program.name}"

    program.delete()

    messages.success(
        request,
        f'Образовательная программа "{name}" '
        f'окончательно удалена из базы данных.'
    )

    return redirect("educational_program_archive")