from django.urls import path

from .views import students
from .views import education_history
from .views import contact_person

urlpatterns = [
    path(
        "",
        students.student_list,
        name="student_list",
    ),
    path(
        "add/",
        students.student_create,
        name="student_create",
    ),
    path(
        "archive/",
        students.student_archive,
        name="student_archive",
    ),
    path(
        "<int:pk>/",
        students.student_detail,
        name="student_detail",
    ),
    path(
        "<int:pk>/edit/",
        students.student_edit,
        name="student_edit",
    ),
    path(
        "<int:pk>/delete/",
        students.student_delete,
        name="student_delete",
    ),
    path(
        "<int:pk>/restore/",
        students.student_restore,
        name="student_restore",
    ),
    path(
        "<int:pk>/delete-forever/",
        students.student_delete_forever,
        name="student_delete_forever",
    ),
    path(
        "<int:student_pk>/education-history/",
        education_history.education_history_list,
        name="education_history_list",
    ),
    path(
        "<int:student_pk>/education-history/add/",
        education_history.education_history_create,
        name="education_history_create",
    ),
    path(
        "education-history/<int:pk>/edit/",
        education_history.education_history_edit,
        name="education_history_edit",
    ),
    path(
        "education-history/<int:pk>/delete/",
        education_history.education_history_delete,
        name="education_history_delete",
    ),
    path(
        "<int:student_pk>/contact-person/add/",
        contact_person.contact_person_create,
        name="contact_person_create",
    ),
]