document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".auto-submit").forEach(select => {

        select.addEventListener("change", () => {
            select.form.submit();
        });

    });

});