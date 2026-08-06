document.addEventListener("DOMContentLoaded", function () {

    const statusField = document.getElementById("id_study_status");
    const expulsionRow = document.getElementById("expulsion-row");

    function toggleReason() {

        if (!statusField || !expulsionRow) return;

        if (statusField.value === "expelled") {
            expulsionRow.style.display = "";
        } else {
            expulsionRow.style.display = "none";
        }
    }

    if (statusField) {
        statusField.addEventListener("change", toggleReason);
        toggleReason();
    }

    const snilsInput = document.getElementById("id_snils");
    if (snilsInput) {
        IMask(snilsInput, {
            mask: "000-000-000 00",
        });
    }

    const phoneInput = document.getElementById("id_phone");
    if (phoneInput) {
        IMask(phoneInput, {
            mask: "+{7} (000) 000-00-00",
        });
    }

});