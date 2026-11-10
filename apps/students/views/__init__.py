from .students import (
    student_list,
    student_detail,
    student_create,
    student_edit,
    student_delete,
    student_archive,
    student_restore,
    student_delete_forever,
)

from .education_history import (
    education_history_list,
    education_history_create,
    education_history_edit,
    education_history_delete
)

from .contact_person import (
    contact_person_create,
    contact_person_edit,
    contact_person_delete
)

from .student_questionnaire import student_questionnaire
from .disability_certificate import disability_certificate_create, disability_certificate_history, disability_certificate_edit
from .student_special_needs import student_special_needs
from .student_special_conditions import student_special_conditions