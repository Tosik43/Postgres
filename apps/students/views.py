from django.db.models import Q
from django.shortcuts import render
from .models import Student
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import StudentForm
from django.contrib import messages
from django.utils import timezone

def student_list(request):

    query = request.GET.get("q", "")
    students = Student.objects.filter(is_active=True)

    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(snils__icontains=query)
        )

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "query": query
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