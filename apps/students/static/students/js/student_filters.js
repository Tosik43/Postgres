document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.querySelector('input[name="q"]');
    const studentTableBody = document.getElementById("student-table-body");
    const filterForm = searchInput
        ? searchInput.closest("form")
        : document.querySelector("form");

    if (!filterForm || !studentTableBody) {
        return;
    }


    let searchTimeout;

    if (searchInput) {

        searchInput.addEventListener("input", () => {

            clearTimeout(searchTimeout);

            searchTimeout = setTimeout(() => {

                performSearch();

            }, 100);

        });

    }


    function performSearch(updateUrl = true) {

        const params = new URLSearchParams(
            new FormData(filterForm)
        );

        const currentUrl = new URL(window.location.href);

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

            const tableHead =
                document.getElementById("student-table-head");

            if (tableHead && data.thead) {
                tableHead.innerHTML = data.thead;
            }

            // Обновляем строки
            studentTableBody.innerHTML =
                data.tbody;

            if (updateUrl) {

                window.history.replaceState(
                    {},
                    "",
                    data.url
                );

            }

            initAjaxSort();

        })
        .catch(error => {

            console.error(
                "Ошибка фильтрации:",
                error
            );

        });
    }

    function initAjaxSort() {

        document
            .querySelectorAll(".ajax-sort")
            .forEach(link => {

                link.addEventListener("click", function (event) {

                    event.preventDefault();

                    fetch(
                        this.href,
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

                        document.getElementById(
                            "student-table-head"
                        ).innerHTML = data.thead;

                        document.getElementById(
                            "student-table-body"
                        ).innerHTML = data.tbody;

                        window.history.pushState(
                            {},
                            "",
                            data.url
                        );

                        initAjaxSort();

                    })
                    .catch(error => {

                        console.error(
                            "Ошибка сортировки:",
                            error
                        );

                    });

                });

            });

    }

    initAjaxSort();

    filterForm
        .querySelectorAll(".auto-submit")
        .forEach(select => {

            select.addEventListener(
                "change",
                function () {

                    performSearch();

                }
            );

        });

    const resetButton =
        document.getElementById("reset-student-filters");

    if (resetButton) {

        resetButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                const searchInput =
                    filterForm.querySelector(
                        'input[name="q"]'
                    );

                if (searchInput) {
                    searchInput.value = "";
                }

                filterForm
                    .querySelectorAll("select")
                    .forEach(select => {
                        select.value = "";
                    });

                // Удаляем сортировку из URL
                const resetUrl =
                    window.location.pathname;

                fetch(
                    resetUrl,
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

                    document.getElementById(
                        "student-table-head"
                    ).innerHTML = data.thead;

                    document.getElementById(
                        "student-table-body"
                    ).innerHTML = data.tbody;

                    window.history.replaceState(
                        {},
                        "",
                        resetUrl
                    );

                    // Заново подключаем сортировку
                    initAjaxSort();

                })
                .catch(error => {

                    console.error(
                        "Ошибка сброса фильтров:",
                        error
                    );

                });

            }
        );

    }

});