document.addEventListener("DOMContentLoaded", function () {

    console.log("Application loaded");

    document.querySelectorAll('.auto-submit').forEach(function(select) {
        select.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });

    const studentForeverModal =
        document.getElementById("deleteStudentForeverModal");

    if (studentForeverModal) {

        studentForeverModal.addEventListener(
            "show.bs.modal",
            function (event) {

                const button = event.relatedTarget;

                document.getElementById(
                    "studentForeverName"
                ).textContent = button.dataset.name;

                document.getElementById(
                    "deleteStudentForeverForm"
                ).action = button.dataset.url;

            }
        );

    }

    const facultyModal =
        document.getElementById("deleteFacultyModal");

    if (facultyModal) {

        facultyModal.addEventListener(
            "show.bs.modal",
            function (event) {

                const button = event.relatedTarget;

                document.getElementById(
                    "facultyName"
                ).textContent = button.dataset.name;

                document.getElementById(
                    "deleteFacultyForm"
                ).action = button.dataset.url;

            }
        );

    }

    const facultyForeverModal =
        document.getElementById("deleteFacultyForeverModal");

    if (facultyForeverModal) {

        facultyForeverModal.addEventListener(
            "show.bs.modal",
            function (event) {

                const button = event.relatedTarget;

                document.getElementById(
                    "facultyForeverName"
                ).textContent = button.dataset.name;

                document.getElementById(
                    "deleteFacultyForeverForm"
                ).action = button.dataset.url;

            }
        );

    }

    const educationalProgramModal =
        document.getElementById(
            "deleteEducationalProgramModal"
        );

    if (educationalProgramModal) {

        educationalProgramModal.addEventListener(
            "show.bs.modal",
            function (event) {

                const button = event.relatedTarget;

                document.getElementById(
                    "educationalProgramName"
                ).textContent = button.dataset.name;

                document.getElementById(
                    "deleteEducationalProgramForm"
                ).action = button.dataset.url;

            }
        );

    }

    const educationalProgramForeverModal =
        document.getElementById(
            "deleteEducationalProgramForeverModal"
        );

        if (educationalProgramForeverModal) {

        educationalProgramForeverModal.addEventListener(
            "show.bs.modal",
            function (event) {

                const button = event.relatedTarget;

                document.getElementById(
                    "deleteEducationalProgramForeverName"
                ).textContent = button.dataset.name;

                document.getElementById(
                    "deleteEducationalProgramForeverForm"
                ).action = button.dataset.url;

            }
        );

    }

        const statusField = document.getElementById("id_status");
    const changeReasonsBlock = document.getElementById("change-reasons-block");

    if (statusField && changeReasonsBlock) {

        function updateChangeReasonsVisibility() {

            if (
                !statusField.value ||
                statusField.value === "studying"
            ) {
                changeReasonsBlock.style.display = "none";

                changeReasonsBlock
                    .querySelectorAll("input[type='checkbox']")
                    .forEach(function (checkbox) {
                        checkbox.checked = false;
                    });

            } else {
                changeReasonsBlock.style.display = "";
            }
        }

        statusField.addEventListener(
            "change",
            updateChangeReasonsVisibility
        );

        updateChangeReasonsVisibility();
    }

    const deleteEducationHistoryModal =
        document.getElementById(
            "deleteEducationHistoryModal"
        );

    if (deleteEducationHistoryModal) {

        const deleteEducationHistoryForm =
            document.getElementById(
                "deleteEducationHistoryForm"
            );

        const educationHistoryRecordName =
            document.getElementById(
                "educationHistoryRecordName"
            );

        deleteEducationHistoryModal.addEventListener(
            "show.bs.modal",
            function (event) {

                const button = event.relatedTarget;

                educationHistoryRecordName.textContent =
                    button.dataset.name;

                deleteEducationHistoryForm.action =
                    button.dataset.url;

            }
        );

    }

});