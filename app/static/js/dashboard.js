/* FILTERING */
const filterInput = document.getElementById("filterInput");
const tableBody = document
    .getElementById("logTable")
    .getElementsByTagName("tbody")[0];

filterInput.addEventListener("keyup", () => {
    const filter = filterInput.value.toLowerCase();
    const rows = tableBody.getElementsByTagName("tr");

    for (let row of rows) {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(filter) ? "" : "none";
    }
});

/* SORTING */
document.querySelectorAll("#logTable th").forEach(th => {
    th.addEventListener("click", () => {
        const table = th.closest("table");
        const tbody = table.querySelector("tbody");
        const index = Array.from(th.parentNode.children).indexOf(th);

        const rows = Array.from(tbody.querySelectorAll("tr"));

        const desc = th.classList.contains("sorted-asc");

        // Clear classes
        table.querySelectorAll("th").forEach(h => h.classList.remove("sorted-asc", "sorted-desc"));

        th.classList.toggle("sorted-desc", !desc);
        th.classList.toggle("sorted-asc", desc);

        rows.sort((a, b) => {
            const A = a.children[index].innerText.toLowerCase();
            const B = b.children[index].innerText.toLowerCase();

            // Numeric test
            const numA = parseFloat(A);
            const numB = parseFloat(B);

            if (!isNaN(numA) && !isNaN(numB)) {
                return desc ? numB - numA : numA - numB;
            }

            return desc ? B.localeCompare(A) : A.localeCompare(B);
        });

        // Apply sorted rows
        rows.forEach(r => tbody.appendChild(r));
    });
});
