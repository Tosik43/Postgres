from django.db.models import (
    Q,
    OuterRef,
    Subquery,
    Case,
    When,
    Value,
    IntegerField,
)

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string

from ..models import (
    Student,
    Gender,
    EducationHistory,
    EducationHistoryStatus,
)

from ..forms import StudentForm

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

    latest_education = (
        EducationHistory.objects
        .filter(
            student=OuterRef("pk")
        )
        .order_by(
            "-start_date",
            "-id"
        )
    )

    students = (
        Student.objects
        .filter(
            is_active=True
        )
        .annotate(
            current_status=Subquery(
                latest_education.values("status")[:1]
            ),
            current_start_date=Subquery(
                latest_education.values("start_date")[:1]
            ),
            current_end_date=Subquery(
                latest_education.values("end_date")[:1]
            ),
            current_expulsion_reason=Subquery(
                latest_education.values("expulsion_reason")[:1]
            ),
            education_enrollment_year=Subquery(
                EducationHistory.objects
                .filter(
                    student=OuterRef("pk")
                )
                .order_by(
                    "start_date",
                    "id"
                )
                .values("start_date__year")[:1]
            )
        )
    )

    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(snils__icontains=query)
        )

    if status == EducationHistoryStatus.STUDYING:
        students = students.filter(
            current_status__in=[
                EducationHistoryStatus.STUDYING,
                EducationHistoryStatus.TRANSFERRED,
            ]
        )

    elif status:
        students = students.filter(
            current_status=status
        )

    if gender:
        students = students.filter(
            gender=gender
        )

    if year:
        students = students.filter(
            education_enrollment_year=year
        )

    allowed_sort_fields = {
        "full_name": "full_name",
        "snils": "snils",
        "study_status": "current_status",
        "enrollment_year": "education_enrollment_year",
    }

    sort_field = allowed_sort_fields.get(sort)

    if sort == "study_status":

        students = students.annotate(
            status_sort_order=Case(
                When(
                    current_status="academic_leave",
                    then=Value(1),
                ),
                When(
                    current_status="graduated",
                    then=Value(2),
                ),
                When(
                    current_status__in=[
                        "studying",
                        "transferred",
                    ],
                    then=Value(3),
                ),
                When(
                    current_status="expelled",
                    then=Value(4),
                ),
                default=Value(99),
                output_field=IntegerField(),
            )
        )

        if direction == "desc":
            students = students.order_by(
                "-status_sort_order"
            )
        else:
            students = students.order_by(
                "status_sort_order"
            )

    elif sort_field:

        if direction == "desc":
            students = students.order_by(
                f"-{sort_field}"
            )
        else:
            students = students.order_by(
                sort_field
            )

    years = (
        Student.objects
        .filter(is_active=True)
        .annotate(
            first_education_year=Subquery(
                EducationHistory.objects
                .filter(
                    student=OuterRef("pk")
                )
                .order_by(
                    "start_date",
                    "id"
                )
                .values("start_date__year")[:1]
            )
        )
        .values_list(
            "first_education_year",
            flat=True
        )
        .exclude(
            first_education_year__isnull=True
        )
        .distinct()
        .order_by("-first_education_year")
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
            "status_choices": EducationHistoryStatus.choices,
            "gender": gender,
            "gender_choices": Gender.choices,
            "year": year,
            "years": years,
            "sort": sort,
            "direction": direction,
            
        }
    )

def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    active_tab = request.GET.get("tab", "contacts")

    current_education = (
        student.education_history
        .select_related(
            "faculty",
            "educational_program",
        )
        .order_by("-start_date")
        .first()
    )

    first_education = (
        student.education_history
        .order_by("start_date")
        .first()
    )

    last_finished_education = (
        student.education_history
        .filter(
            end_date__isnull=False,
            status__in=[
                EducationHistoryStatus.EXPELLED,
                EducationHistoryStatus.GRADUATED,
            ],
        )
        .order_by("-end_date")
        .first()
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
            "current_education": current_education,
            "first_education": first_education,
            "last_finished_education": last_finished_education,
            "active_tab": active_tab,
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