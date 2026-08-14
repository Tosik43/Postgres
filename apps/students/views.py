from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Student, StudyStatus, Gender
from .forms import StudentForm, EducationHistoryForm
from .education_history import EducationHistory
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string

def student_list(request):

    query = request.GET.get("q", "")
    status = request.GET.get("status", "")
    gender = request.GET.get("gender", "")
    year = request.GET.get("year", "")
    sort = request.GET.get("sort", "")
    direction = request.GET.get("direction", "asc")

    query_params = request.GET.copy()

    query_params.pop("sort", None)
    query_params.pop("direction", None)

    students = Student.objects.filter(
        is_active=True
    )

    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(snils__icontains=query)
        )

    if status:
        students = students.filter(
            study_status=status
        )

    if gender:
        students = students.filter(
            gender=gender
        )

    if year:
        students = students.filter(
            enrollment_year=year
        )

    allowed_sort_fields = {
        "full_name": "full_name",
        "snils": "snils",
        "study_status": "study_status",
        "enrollment_year": "enrollment_year",
    }

    sort_field = allowed_sort_fields.get(sort)

    if sort_field:
        if direction == "desc":
            students = students.order_by(f"-{sort_field}")
        else:
            students = students.order_by(sort_field)

    years = (
        Student.objects
        .filter(is_active=True)
        .values_list(
            "enrollment_year",
            flat=True
        )
        .distinct()
        .order_by("-enrollment_year")
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        tbody = render_to_string(
            "students/partials/student_table_body.html",
            {
                "students": students,
            },
            request=request,
        )

        thead = render_to_string(
            "students/student_table_head.html",
            {
                "query": query,
                "status": status,
                "gender": gender,
                "year": year,
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

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "query": query,
            "status": status,
            "status_choices": StudyStatus.choices,
            "gender": gender,
            "gender_choices": Gender.choices,
            "year": year,
            "years": years,
            "sort": sort,
            "direction": direction,
            
        }
    )

def student_search(request):

    query = request.GET.get("q", "")
    status = request.GET.get("status", "")
    gender = request.GET.get("gender", "")
    year = request.GET.get("year", "")

    students = Student.objects.filter(
        is_active=True
    )

    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(snils__icontains=query)
        )

    if status:
        students = students.filter(
            study_status=status
        )

    if gender:
        students = students.filter(
            gender=gender
        )

    if year:
        students = students.filter(
            enrollment_year=year
        )

    return render(
        request,
        "students/partials/student_table_body.html",
        {
            "students": students,
        }
    )

def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student
        }
    )

def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()

            messages.success(
                request,
                "Студент успешно добавлен."
            )

            return redirect(
                "student_detail",
                pk=student.pk
            )
    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "student": None,          
        }
    )

def student_edit(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Данные студента успешно сохранены."
            )

            return redirect(
                "student_detail",
                pk=student.pk
            )

    else:

        form = StudentForm(instance=student)

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "student": student,
        }
    )

def student_delete(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk,
        is_active=True
    )

    if request.method == "POST":

        student.is_active = False
        student.deleted_at = timezone.now()
        student.save()

        messages.success(
            request,
            f'Студент "{student.full_name}" успешно удален.'
        )

    return redirect("student_list")

def student_archive(request):

    students = Student.objects.filter(
        is_active=False
    ).order_by("-deleted_at")

    return render(
        request,
        "students/student_archive.html",
        {
            "students": students
        }
    )

def student_restore(request, pk):

    if request.method != "POST":
        return redirect("student_archive")

    student = get_object_or_404(
        Student,
        pk=pk,
        is_active=False
    )

    student.is_active = True
    student.deleted_at = None
    student.save()

    messages.success(
        request,
        "Студент успешно восстановлен."
    )

    return redirect("student_archive")

def student_delete_forever(request, pk):

    if request.method != "POST":
        return redirect("student_archive")

    student = get_object_or_404(
        Student,
        pk=pk,
        is_active=False
    )

    name = student.full_name

    student.delete()

    messages.success(
        request,
        f'Студент "{name}" окончательно удален из базы данных.'
    )

    return redirect("student_archive")

def education_history_list(request, student_pk):
    student = get_object_or_404(
        Student,
        pk=student_pk
    )

    history = (
        EducationHistory.objects
        .filter(student=student)
        .select_related(
            "faculty",
            "educational_program"
        )
        .prefetch_related("change_reasons")
        .order_by(
            "academic_year",
            "course",
            "semester"
        )
    )

    return render(
        request,
        "students/education_history/list.html",
        {
            "student": student,
            "history": history,
        }
    )


def education_history_create(request, student_pk):
    student = get_object_or_404(
        Student,
        pk=student_pk
    )

    if request.method == "POST":

        form = EducationHistoryForm(
            request.POST
        )

        form.instance.student = student

        if form.is_valid():

            history = form.save()

            messages.success(
                request,
                "Запись истории обучения успешно добавлена."
            )

            return redirect(
                "education_history_list",
                student_pk=student.pk
            )

    else:

        form = EducationHistoryForm()

    return render(
        request,
        "students/education_history/form.html",
        {
            "form": form,
            "student": student,
            "history_record": None,
        }
    )

def education_history_edit(request, pk):
    history_record = get_object_or_404(
        EducationHistory,
        pk=pk
    )

    if request.method == "POST":
        form = EducationHistoryForm(
            request.POST,
            instance=history_record
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Запись истории обучения успешно сохранена."
            )

            return redirect(
                "education_history_list",
                student_pk=history_record.student.pk
            )

    else:
        form = EducationHistoryForm(
            instance=history_record
        )

    return render(
        request,
        "students/education_history/form.html",
        {
            "form": form,
            "student": history_record.student,
            "history_record": history_record,
        }
    )


def education_history_delete(request, pk):
    history_record = get_object_or_404(
        EducationHistory,
        pk=pk
    )

    student_pk = history_record.student.pk

    if request.method == "POST":
        history_record.delete()

        messages.success(
            request,
            "Запись истории обучения удалена."
        )

    return redirect(
        "education_history_list",
        student_pk=student_pk
    )