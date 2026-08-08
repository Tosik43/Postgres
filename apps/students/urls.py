from django.urls import path

from . import views

urlpatterns = [

    path("",
        views.student_list, 
        name="student_list"
    ),
    path(
        "<int:pk>/",
        views.student_detail,
        name="student_detail",
    ),
    path(
        "<int:pk>/edit/",
        views.student_edit,
        name="student_edit",
    ),
    path(
        "add/", 
        views.student_create, 
        name="student_create"
    ),
    path(
        "<int:pk>/delete/",
        views.student_delete,
        name="student_delete",
    ),
    path(
        "archive/",
        views.student_archive,
        name="student_archive",
    ),
    path(
        "<int:pk>/restore/",
        views.student_restore,
        name="student_restore",
    ),
    path(
        "references/",
        views.reference_list,
        name="reference_list",
    ),
    path(
        "faculties/",
        views.faculty_list,
        name="faculty_list",
    ),
]

