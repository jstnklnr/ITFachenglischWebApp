function createTable(solution) {
    let table = document.getElementById("solution");
    let n = solution.length;
    let html = "";

    for(let y = 0; y < n; y++) {
        html += "<tr>";

        for(let x = 0; x < n; x++) {
            html += `<td ${(x + y + 1) % 2 == 0 ? "class='black'" : ""}>`;

            if(x == solution[y])
                html += "&#9813";

            html += "</td>";
        }

        html += "</tr>";
    }

    table.innerHTML = html;
}