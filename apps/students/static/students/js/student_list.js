document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("deleteModal");

    modal.addEventListener("show.bs.modal", function (event) {

        const button = event.relatedTarget;

        document.getElementById("studentName").textContent =
            button.dataset.name;

        document.getElementById("deleteForm").action =
            button.dataset.url;

    });

});