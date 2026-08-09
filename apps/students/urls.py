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
        "students/<int:pk>/delete-forever/",
        views.student_delete_forever,
        name="student_delete_forever"
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
    path(
        "faculties/add/",
        views.faculty_create,
        name="faculty_create",
    ),
    path(
        "faculties/<int:pk>/edit/",
        views.faculty_edit,
        name="faculty_edit"
    ),
    path(
        "faculties/<int:pk>/delete/",
        views.faculty_delete,
        name="faculty_delete"
    ),
    path(
        "faculties/archive/",
        views.faculty_archive,
        name="faculty_archive"
    ),

    path(
        "faculties/<int:pk>/restore/",
        views.faculty_restore,
        name="faculty_restore"
    ),
    path(
        "faculties/<int:pk>/delete-forever/",
        views.faculty_delete_forever,
        name="faculty_delete_forever"
    ),
]

