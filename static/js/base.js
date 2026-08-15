document.addEventListener("DOMContentLoaded", function () {

    console.log("Application loaded");

    document
    .querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach(function (element) {
        new bootstrap.Tooltip(element);
    });


    const educationalProgramSelect =
        document.querySelector(".searchable-program");

    if (educationalProgramSelect) {

        new TomSelect(
            educationalProgramSelect,
            {

                placeholder:
                    "Выберите образовательную программу",

                searchField: [
                    "text"
                ],

                allowEmptyOption: false,

                maxOptions: 50,

                closeAfterSelect: true,

                onInitialize: function () {

                    this.clear(true);

                    this.control_input.placeholder =
                        "Выберите образовательную программу";

                },

                onFocus: function () {

                    if (!this.getValue()) {

                        this.clear(true);

                        this.control_input.value = "";

                        this.control_input.placeholder = "";

                    }

                },

                onChange: function (value) {

                    if (value) {

                        this.control_input.placeholder = "";

                    } else {

                        this.control_input.placeholder =
                            "Выберите образовательную программу";

                    }

                }

            }
        );

    }

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
                statusField.value === "studying" ||
                statusField.value === "graduated" ||
                statusField.value === "expelled"
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

    const educationStatusField =
        document.getElementById("id_status");

    const expulsionReasonBlock =
        document.getElementById("expulsion-reason-block");

    if (educationStatusField && expulsionReasonBlock) {

        function updateExpulsionReasonVisibility() {

            if (educationStatusField.value === "expelled") {

                expulsionReasonBlock.style.display = "";

            } else {

                expulsionReasonBlock.style.display = "none";

                const reasonField =
                    expulsionReasonBlock.querySelector("input, textarea");

                if (reasonField) {
                    reasonField.value = "";
                }

            }
        }

        educationStatusField.addEventListener(
            "change",
            updateExpulsionReasonVisibility
        );

        updateExpulsionReasonVisibility();
    }

});