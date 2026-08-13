document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".auto-submit").forEach(select => {

        select.addEventListener("change", () => {
            select.form.submit();
        });

    });


    const searchInput =
        document.getElementById("student-search");

    if (searchInput) {

        let searchTimer;

        searchInput.addEventListener("input", () => {

            clearTimeout(searchTimer);

            searchTimer = setTimeout(() => {

                searchInput.form.submit();

            }, 300);

        });

    }

});