
async function loadStats() {
    const res = await fetch("http://192.168.1.43:5000/api/stats");
    const data = await res.json();
    let html = "<ul>";
    data.forEach(row => html += `<li>${row.service}: ${row.count}</li>`);
    html += "</ul>";
    document.getElementById("stats").innerHTML = html;
}

async function loadLogs() {
    const res = await fetch("http://192.168.1.43:5000/api/logs?limit=20");
    const data = await res.json();
    const tbody = document.querySelector("#logTable tbody");
    tbody.innerHTML = "";
    data.forEach(log => {
        tbody.innerHTML += `<tr>
            <td>${log.timestamp}</td>
            <td>${log.service}</td>
            <td>${log.message}</td>
        </tr>`;
    });
}

loadStats();
loadLogs();
setInterval(loadLogs, 5000);  // auto-refresh every 5s