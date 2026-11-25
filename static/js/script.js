
// ==============================
// CURRENT DATE
// ==============================

const dateElement = document.getElementById("currentDate");

if (dateElement) {

    const today = new Date();

    dateElement.textContent = today.toLocaleDateString("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric"
    });

}


// ==============================
// ADD STUDENT FORM
// ==============================

function openStudentForm() {

    const form = document.getElementById("studentForm");

    if (form) {

        form.classList.add("show");

        form.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

        document.getElementById("name").focus();

    }

}


function closeStudentForm() {

    const form = document.getElementById("studentForm");

    if (form) {
        form.classList.remove("show");
    }

}


// ==============================
// STUDENT SEARCH
// ==============================

const searchInput = document.getElementById("studentSearch");

if (searchInput) {

    searchInput.addEventListener("input", function () {

        const searchValue = this.value.toLowerCase().trim();

        const rows = document.querySelectorAll(
            "#studentTable tbody tr"
        );

        let visibleCount = 0;

        rows.forEach(row => {

            const rowText = row.textContent.toLowerCase();

            const match = rowText.includes(searchValue);

            row.style.display = match ? "" : "none";

            if (match) {
                visibleCount++;
            }

        });

        const noResults = document.getElementById("noResults");

        if (noResults) {

            noResults.style.display =
                visibleCount === 0 ? "block" : "none";

        }

    });

}


// ==============================
// DELETE CONFIRMATION
// ==============================

function confirmDelete(studentName) {

    return confirm(
        `Are you sure you want to delete ${studentName}'s record?`
    );

}


// ==============================
// AUTO DISMISS FLASH MESSAGES
// ==============================

document.addEventListener("DOMContentLoaded", function () {

    const messages = document.querySelectorAll(".flash-message");

    messages.forEach(message => {

        setTimeout(() => {

            message.style.transition = "opacity 0.5s";

            message.style.opacity = "0";

            setTimeout(() => {
                message.remove();
            }, 500);

        }, 4000);

    });

});
// =================================
// COURSES SECTION
// =================================

// Open course form
function openCourseForm() {
    const form = document.getElementById("courseForm");

    if (form) {
        form.classList.add("show");

        form.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    }
}


// Close course form
function closeCourseForm() {
    const form = document.getElementById("courseForm");

    if (form) {
        form.classList.remove("show");
    }
}


// Course search functionality
const courseSearch = document.getElementById("courseSearch");

if (courseSearch) {

    courseSearch.addEventListener("input", function () {

        const searchValue = this.value.toLowerCase();

        const rows = document.querySelectorAll(
            "#courseTable tbody tr"
        );

        let visibleCount = 0;

        rows.forEach(function (row) {

            const match = row.textContent
                .toLowerCase()
                .includes(searchValue);

            row.style.display = match ? "" : "none";

            if (match) {
                visibleCount++;
            }

        });

        const message = document.getElementById("noCourseResults");

        if (message) {
            message.style.display =
                visibleCount === 0 ? "block" : "none";
        }

    });

}
