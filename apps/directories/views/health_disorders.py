from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

from ..models import HealthDisorder
from ..forms import HealthDisorderForm


def health_disorder_list(request):

    query = request.GET.get("q", "").strip()

    sort = request.GET.get("sort", "")
    direction = request.GET.get("direction", "asc")

    disorders = HealthDisorder.objects.filter(
        is_active=True
    )

    # Поиск по названию нарушения
    if query:
        disorders = disorders.filter(
            Q(name__icontains=query) |
            Q(health_features__icontains=query)
        )

    # Разрешённые поля сортировки
    allowed_sort_fields = {
        "name": "name",
        "health_features": "health_features",
    }

    sort_field = allowed_sort_fields.get(sort)

    if sort_field:

        if direction == "desc":

            disorders = disorders.order_by(
                f"-{sort_field}"
            )

        else:

            disorders = disorders.order_by(
                sort_field
            )

    else:

        disorders = disorders.order_by(
            "name"
        )

    context = {
        "disorders": disorders,
        "query": query,
        "sort": sort,
        "direction": direction,
    }

    # AJAX-запрос
    if request.headers.get(
        "X-Requested-With"
    ) == "XMLHttpRequest":

        tbody = render_to_string(
            "directories/health_disorders/partials/health_disorder_table_body.html",
            {
                "disorders": disorders,
            },
            request=request,
        )

        thead = render_to_string(
            "directories/health_disorders/health_disorder_table_head.html",
            {
                "query": query,
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
        "directories/health_disorders/list.html",
        context
    )


def health_disorder_create(request):

    if request.method == "POST":

        form = HealthDisorderForm(
            request.POST
        )

        if form.is_valid():

            disorder = form.save()

            messages.success(
                request,
                f'Вид нарушения "{disorder.name}" '
                f'успешно добавлен.'
            )

            return redirect(
                "health_disorder_list"
            )

    else:

        form = HealthDisorderForm()

    return render(
        request,
        "directories/health_disorders/form.html",
        {
            "form": form,
            "disorder": None,
        }
    )


def health_disorder_edit(request, pk):

    disorder = get_object_or_404(
        HealthDisorder,
        pk=pk,
        is_active=True
    )

    if request.method == "POST":

        form = HealthDisorderForm(
            request.POST,
            instance=disorder
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Вид нарушения успешно сохранён."
            )

            return redirect(
                "health_disorder_list"
            )

    else:

        form = HealthDisorderForm(
            instance=disorder
        )

    return render(
        request,
        "directories/health_disorders/form.html",
        {
            "form": form,
            "disorder": disorder,
        }
    )


def health_disorder_delete(request, pk):

    disorder = get_object_or_404(
        HealthDisorder,
        pk=pk,
        is_active=True
    )

    if request.method == "POST":

        disorder.is_active = False
        disorder.deleted_at = timezone.now()
        disorder.save()

        messages.success(
            request,
            f'Вид нарушения "{disorder.name}" '
            f'успешно удалён.'
        )

    return redirect(
        "health_disorder_list"
    )


def health_disorder_archive(request):

    disorders = (
        HealthDisorder.objects
        .filter(is_active=False)
        .order_by("-deleted_at")
    )

    return render(
        request,
        "directories/health_disorders/archive.html",
        {
            "disorders": disorders,
        }
    )


def health_disorder_restore(request, pk):

    if request.method != "POST":

        return redirect(
            "health_disorder_archive"
        )

    disorder = get_object_or_404(
        HealthDisorder,
        pk=pk,
        is_active=False
    )

    disorder.is_active = True
    disorder.deleted_at = None
    disorder.save()

    messages.success(
        request,
        "Вид нарушения успешно восстановлен."
    )

    return redirect(
        "health_disorder_archive"
    )


def health_disorder_delete_forever(request, pk):

    if request.method != "POST":

        return redirect(
            "health_disorder_archive"
        )

    disorder = get_object_or_404(
        HealthDisorder,
        pk=pk,
        is_active=False
    )

    name = disorder.name

    disorder.delete()

    messages.success(
        request,
        f'Вид нарушения "{name}" '
        f'окончательно удалён из базы данных.'
    )

    return redirect(
        "health_disorder_archive"
    )