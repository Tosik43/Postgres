document.addEventListener("DOMContentLoaded", function () {

    console.log("Application loaded");

    document
    .querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach(function (element) {
        new bootstrap.Tooltip(element);
    });

    document
    .querySelectorAll('[data-bs-tooltip]')
    .forEach(function (element) {
        new bootstrap.Tooltip(element, {
            title: element.dataset.bsTooltip
        });
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

                    if (!this.getValue()) {

                        this.control_input.placeholder =
                            "Выберите образовательную программу";

                    }

                },

                onFocus: function () {

                    if (!this.getValue()) {

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

    const deleteContactModal =
        document.getElementById(
            "deleteContactModal"
        );

    if (deleteContactModal) {

        const deleteContactForm =
            document.getElementById(
                "deleteContactForm"
            );

        const deleteContactName =
            document.getElementById(
                "deleteContactName"
            );

        deleteContactModal.addEventListener(
            "show.bs.modal",
            function (event) {

                const button = event.relatedTarget;

                deleteContactName.textContent =
                    button.dataset.contactName;

                deleteContactForm.action =
                    button.dataset.deleteUrl;

            }
        );

    }

    const programSearchForm =
        document.getElementById("programSearchForm");

    if (programSearchForm) {

        const searchInput =
            document.getElementById("search");

        const educationLevel =
            document.getElementById("education_level");

        let searchTimeout;


        function loadPrograms(params, updateUrl = true) {

            fetch(
                `${window.location.pathname}?${params.toString()}`,
                {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                }
            )
            .then(response => {

                if (!response.ok) {
                    throw new Error(
                        `HTTP error: ${response.status}`
                    );
                }

                return response.json();

            })
            .then(data => {

                const tableHead =
                    document.getElementById(
                        "program-table-head"
                    );

                const tableBody =
                    document.getElementById(
                        "programTableBody"
                    );


                if (tableHead && data.thead) {

                    tableHead.innerHTML =
                        data.thead;

                }


                if (tableBody && data.tbody) {

                    tableBody.innerHTML =
                        data.tbody;

                }


                if (updateUrl) {

                    window.history.replaceState(
                        {},
                        "",
                        data.url
                    );

                }


                initProgramAjaxSort();

            })
            .catch(error => {

                console.error(
                    "Ошибка загрузки образовательных программ:",
                    error
                );

            });

        }


        function performProgramSearch() {

            const params =
                new URLSearchParams(
                    new FormData(programSearchForm)
                );


            const currentUrl =
                new URL(window.location.href);


            const currentSort =
                currentUrl.searchParams.get("sort");

            const currentDirection =
                currentUrl.searchParams.get("direction");


            if (currentSort) {

                params.set(
                    "sort",
                    currentSort
                );

            }


            if (currentDirection) {

                params.set(
                    "direction",
                    currentDirection
                );

            }


            loadPrograms(params);

        }


        if (searchInput) {

            searchInput.addEventListener(
                "input",
                function () {

                    clearTimeout(
                        searchTimeout
                    );

                    searchTimeout =
                        setTimeout(
                            performProgramSearch,
                            100
                        );

                }
            );

        }


        if (educationLevel) {

            educationLevel.addEventListener(
                "change",
                function () {

                    performProgramSearch();

                }
            );

        }


        programSearchForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();

                performProgramSearch();

            }
        );


        function initProgramAjaxSort() {

            document
                .querySelectorAll(
                    ".ajax-program-sort"
                )
                .forEach(link => {

                    if (
                        link.dataset.ajaxSortInitialized
                    ) {
                        return;
                    }


                    link.dataset.ajaxSortInitialized =
                        "true";


                    link.addEventListener(
                        "click",
                        function (event) {

                            event.preventDefault();


                            fetch(
                                this.href,
                                {
                                    headers: {
                                        "X-Requested-With":
                                            "XMLHttpRequest"
                                    }
                                }
                            )
                            .then(response => {

                                if (!response.ok) {
                                    throw new Error(
                                        `HTTP error: ${response.status}`
                                    );
                                }

                                return response.json();

                            })
                            .then(data => {

                                const tableHead =
                                    document.getElementById(
                                        "program-table-head"
                                    );

                                const tableBody =
                                    document.getElementById(
                                        "programTableBody"
                                    );


                                if (
                                    tableHead &&
                                    data.thead
                                ) {

                                    tableHead.innerHTML =
                                        data.thead;

                                }


                                if (
                                    tableBody &&
                                    data.tbody
                                ) {

                                    tableBody.innerHTML =
                                        data.tbody;

                                }


                                window.history.pushState(
                                    {},
                                    "",
                                    data.url
                                );


                                initProgramAjaxSort();

                            })
                            .catch(error => {

                                console.error(
                                    "Ошибка сортировки образовательных программ:",
                                    error
                                );

                            });

                        }
                    );

                });

        }


        initProgramAjaxSort();

    }

    const healthDisorderSearchForm =
        document.getElementById("healthDisorderSearchForm");

    if (healthDisorderSearchForm) {

        const searchInput =
            document.getElementById("healthDisorderSearch");

        let searchTimeout;


        function performHealthDisorderSearch() {

            const params = new URLSearchParams(
                new FormData(healthDisorderSearchForm)
            );

            const currentUrl =
                new URL(window.location.href);

            const currentSort =
                currentUrl.searchParams.get("sort");

            const currentDirection =
                currentUrl.searchParams.get("direction");


            if (currentSort) {
                params.set("sort", currentSort);
            }

            if (currentDirection) {
                params.set("direction", currentDirection);
            }


            fetch(
                `${window.location.pathname}?${params.toString()}`,
                {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                }
            )
            .then(response => {

                if (!response.ok) {
                    throw new Error(
                        `HTTP error: ${response.status}`
                    );
                }

                return response.json();

            })
            .then(data => {

                const tableBody =
                    document.getElementById(
                        "healthDisorderTableBody"
                    );

                const tableHead =
                    document.getElementById(
                        "health-disorder-table-head"
                    );


                if (tableBody) {
                    tableBody.innerHTML = data.tbody;
                }

                if (tableHead) {
                    tableHead.innerHTML = data.thead;
                }


                window.history.replaceState(
                    {},
                    "",
                    data.url
                );


                initHealthDisorderAjaxSort();

            })
            .catch(error => {

                console.error(
                    "Ошибка фильтрации видов нарушений здоровья:",
                    error
                );

            });

        }


        if (searchInput) {

            searchInput.addEventListener(
                "input",
                function () {

                    clearTimeout(searchTimeout);

                    searchTimeout = setTimeout(
                        performHealthDisorderSearch,
                        100
                    );

                }
            );

        }


        healthDisorderSearchForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();

                performHealthDisorderSearch();

            }
        );


        function initHealthDisorderAjaxSort() {

            document
                .querySelectorAll(
                    ".ajax-health-disorder-sort"
                )
                .forEach(link => {

                    if (link.dataset.ajaxSortInitialized) {
                        return;
                    }

                    link.dataset.ajaxSortInitialized = "true";


                    link.addEventListener(
                        "click",
                        function (event) {

                            event.preventDefault();


                            fetch(
                                this.href,
                                {
                                    headers: {
                                        "X-Requested-With":
                                            "XMLHttpRequest"
                                    }
                                }
                            )
                            .then(response => {

                                if (!response.ok) {
                                    throw new Error(
                                        `HTTP error: ${response.status}`
                                    );
                                }

                                return response.json();

                            })
                            .then(data => {

                                const tableBody =
                                    document.getElementById(
                                        "healthDisorderTableBody"
                                    );

                                const tableHead =
                                    document.getElementById(
                                        "health-disorder-table-head"
                                    );


                                if (tableBody) {
                                    tableBody.innerHTML =
                                        data.tbody;
                                }

                                if (tableHead) {
                                    tableHead.innerHTML =
                                        data.thead;
                                }


                                window.history.pushState(
                                    {},
                                    "",
                                    data.url
                                );


                                initHealthDisorderAjaxSort();

                            })
                            .catch(error => {

                                console.error(
                                    "Ошибка сортировки видов нарушений здоровья:",
                                    error
                                );

                            });

                        }
                    );

                });

        }


        initHealthDisorderAjaxSort();

            const deleteHealthDisorderModal =
                document.getElementById(
                    "deleteHealthDisorderModal"
                );

            if (deleteHealthDisorderModal) {

                deleteHealthDisorderModal.addEventListener(
                    "show.bs.modal",
                    function (event) {

                        const button =
                            event.relatedTarget;

                        if (!button) {
                            return;
                        }

                        const name =
                            button.getAttribute(
                                "data-name"
                            );

                        const url =
                            button.getAttribute(
                                "data-url"
                            );


                        const disorderName =
                            document.getElementById(
                                "healthDisorderName"
                            );

                        const deleteForm =
                            document.getElementById(
                                "deleteHealthDisorderForm"
                            );


                        if (disorderName) {

                            disorderName.textContent =
                                name || "";

                        }

                        if (deleteForm) {

                            deleteForm.action =
                                url || "";

                        }

                    }
                );

            }

        }
    
    const deletePracticeModal =
        document.getElementById(
            "deletePracticeModal"
        );

    if (deletePracticeModal) {

        deletePracticeModal.addEventListener(
            "show.bs.modal",
            function (event) {

                const button =
                    event.relatedTarget;

                if (!button) {
                    return;
                }

                const name =
                    button.getAttribute(
                        "data-name"
                    );

                const url =
                    button.getAttribute(
                        "data-url"
                    );


                const practiceName =
                    document.getElementById(
                        "practiceName"
                    );

                const deleteForm =
                    document.getElementById(
                        "deletePracticeForm"
                    );


                if (practiceName) {

                    practiceName.textContent =
                        name || "";

                }

                if (deleteForm) {

                    deleteForm.action =
                        url || "";

                }

            }
        );

    }

    const deleteContactPersonModal =
        document.getElementById(
            "deleteContactPersonModal"
        );

    if (deleteContactPersonModal) {
        deleteContactPersonModal.addEventListener(
            "show.bs.modal",
            function (event) {

                const button = event.relatedTarget;

                if (!button) {
                    return;
                }

                const name =
                    button.getAttribute("data-name");

                const url =
                    button.getAttribute("data-url");

                const contactPersonName =
                    document.getElementById(
                        "contactPersonName"
                    );

                const deleteForm =
                    document.getElementById(
                        "deleteContactPersonForm"
                    );

                if (contactPersonName) {
                    contactPersonName.textContent =
                        name || "";
                }

                if (deleteForm) {
                    deleteForm.action =
                        url || "";
                }
            }
        );
    }

});