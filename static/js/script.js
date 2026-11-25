/* =====================================
   MEVI MANAGEMENT PORTAL
   JavaScript Functionality
===================================== */


/* =====================================
   LIVE TABLE SEARCH
===================================== */

function setupTableSearch(inputId, tableId) {

    const searchInput = document.getElementById(inputId);
    const table = document.getElementById(tableId);

    // Stop if the search box or table does not exist
    if (!searchInput || !table) {
        return;
    }

    searchInput.addEventListener("input", function () {

        const searchValue = this.value.toLowerCase().trim();

        const rows = table.querySelectorAll("tbody tr");

        rows.forEach(function (row) {

            const rowText = row.textContent.toLowerCase();

            if (rowText.includes(searchValue)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }

        });

    });

}


/* =====================================
   INITIALIZE STUDENT AND COURSE SEARCH
===================================== */

document.addEventListener("DOMContentLoaded", function () {

    setupTableSearch("studentSearch", "studentsTable");

    setupTableSearch("courseSearch", "coursesTable");


    /* =====================================
       AUTOMATIC FLASH MESSAGE DISMISSAL
    ===================================== */

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 4000);

    });


    /* =====================================
       FORM VALIDATION
    ===================================== */

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const requiredInputs = form.querySelectorAll(
                "input[required], textarea[required]"
            );

            let valid = true;

            requiredInputs.forEach(function (input) {

                if (!input.value.trim()) {
                    valid = false;
                    input.style.borderColor = "#e34d59";
                } else {
                    input.style.borderColor = "";
                }

            });

            if (!valid) {
                event.preventDefault();
                alert("Please fill in all required fields.");
            }

        });

    });

});


/* =====================================
   DELETE CONFIRMATION
===================================== */

function confirmDelete(itemName) {

    return confirm(
        "Are you sure you want to delete " +
        itemName +
        "? This action cannot be undone."
    );

}