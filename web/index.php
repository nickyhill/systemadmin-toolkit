<!DOCTYPE html>
<html>
<head>
    <title>Linux Admin Toolkit Dashboard</title>
    <style>
        body { font-family: Arial; background-color: #f4f4f4; margin: 40px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background-color: #ddd; }
    </style>
</head>
<body>
    <h1>System Logs Dashboard</h1>

    <h3>Log Summary</h3>
    <div id="stats"></div>

    <h3>Recent Logs</h3>
    <table id="logTable">
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Service</th>
                <th>Message</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

 <script type="text/javascript" src="scripts/load.js"></script>

</body>
</html>
