document.addEventListener("DOMContentLoaded", function () {

    const select = document.getElementById(
        "id_previous_education_type"
    );

    const otherContainer = document.getElementById(
        "previous-education-other-container"
    );

    function toggleOther() {

        if (select.value === "other") {

            otherContainer.style.display = "block";

        } else {

            otherContainer.style.display = "none";

        }
    }

    select.addEventListener(
        "change",
        toggleOther
    );

    toggleOther();

    const accommodationSelect = document.getElementById(
        "id_accommodation_type"
    );

    const accommodationOtherContainer = document.getElementById(
        "accommodation-other-container"
    );

    function toggleAccommodationOther() {

        if (accommodationSelect.value === "other") {

            accommodationOtherContainer.style.display = "block";

        } else {

            accommodationOtherContainer.style.display = "none";

        }
    }

    accommodationSelect.addEventListener(
        "change",
        toggleAccommodationOther
    );

    toggleAccommodationOther();

    const decisionTimeSelect = document.getElementById(
        "id_decision_time"
    );

    const decisionTimeOtherContainer = document.getElementById(
        "decision-time-other-container"
    );

    function toggleDecisionTimeOther() {

        if (decisionTimeSelect.value === "other") {

            decisionTimeOtherContainer.style.display = "block";

        } else {

            decisionTimeOtherContainer.style.display = "none";

        }
    }

    decisionTimeSelect.addEventListener(
        "change",
        toggleDecisionTimeOther
    );

    toggleDecisionTimeOther();

    const choiceArgumentCheckboxes = document.querySelectorAll(
        'input[name="choice_arguments"]'
    );

    const choiceArgumentsOther = document.getElementById(
        "choice_argument_other"
    );

    const choiceArgumentsOtherContainer = document.getElementById(
        "choice-arguments-other-container"
    );


    function toggleChoiceArgumentsOther() {

        if (choiceArgumentsOther.checked) {

            choiceArgumentsOtherContainer.style.display = "block";

        } else {

            choiceArgumentsOtherContainer.style.display = "none";

        }
    }


    function limitChoiceArguments() {

        const checked = document.querySelectorAll(
            'input[name="choice_arguments"]:checked'
        );

        if (checked.length >= 3) {

            choiceArgumentCheckboxes.forEach(function (checkbox) {

                if (!checkbox.checked) {
                    checkbox.disabled = true;
                }

            });

        } else {

            choiceArgumentCheckboxes.forEach(function (checkbox) {
                checkbox.disabled = false;
            });

        }

    }


    function restoreChoiceArguments() {

        const savedArgumentsElement = document.getElementById(
            "saved-choice-arguments"
        );

        if (!savedArgumentsElement) {
            return;
        }

        const savedArguments = JSON.parse(
            savedArgumentsElement.textContent
        );

        choiceArgumentCheckboxes.forEach(function (checkbox) {

            if (savedArguments.includes(checkbox.value)) {
                checkbox.checked = true;
            }

        });

    }


    choiceArgumentCheckboxes.forEach(function (checkbox) {

        checkbox.addEventListener(
            "change",
            function () {

                toggleChoiceArgumentsOther();

                limitChoiceArguments();

            }
        );

    });


    restoreChoiceArguments();
    toggleChoiceArgumentsOther();
    limitChoiceArguments();

});