from django.urls import path

from . import views

urlpatterns = [

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