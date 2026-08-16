document.addEventListener("DOMContentLoaded", function () {

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