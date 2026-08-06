from django.db.models import Q
from django.shortcuts import render
from .models import Student
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import StudentForm
from django.contrib import messages

def student_list(request):

    query = request.GET.get("q", "")
    students = Student.objects.all()

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