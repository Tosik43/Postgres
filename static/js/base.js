document.addEventListener("DOMContentLoaded", function () {

    console.log("Application loaded");


    const facultyModal =
        document.getElementById("deleteFacultyModal");

    if (facultyModal) {
        facultyModal.addEventListener("show.bs.modal", function (event) {

            const button = event.relatedTarget;

            document.getElementById("facultyName").textContent =
                button.dataset.name;

            document.getElementById("deleteFacultyForm").action =
                button.dataset.url;

        });
    }

});