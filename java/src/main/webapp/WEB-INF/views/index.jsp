<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQLi Labs</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .lab-card {
            margin: 20px 0;
            padding: 20px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background-color: #fafafa;
            transition: all 0.3s ease;
        }
        .lab-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-color: #007bff;
        }
        .lab-card h3 {
            margin-top: 0;
            color: #333;
            margin-bottom: 15px;
        }
        .lab-card p {
            color: #666;
            margin-bottom: 15px;
            line-height: 1.5;
        }
        .lab-link {
            display: inline-block;
            padding: 12px 25px;
            background-color: #dc3545;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .lab-link:hover {
            background-color: #c82333;
            text-decoration: none;
            color: white;
        }
        .lab-type {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        .union { background-color: #007bff; }
        .reflect { background-color: #fd7e14; }
        .boolean { background-color: #6f42c1; }
        .time { background-color: #e83e8c; }

        @media (max-width: 600px) {
            .container {
                padding: 20px;
            }
            .lab-card {
                padding: 15px;
            }
            .lab-link {
                width: 100%;
                text-align: center;
                box-sizing: border-box;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SQLi Labs</h1>

        <div class="lab-card">
            <div class="lab-type union">UNION</div>
            <h3>UNION-based SQL Injection</h3>
            <p>Extract data from multiple tables using UNION SELECT statements to bypass authentication and retrieve sensitive data.</p>
            <a href="union" class="lab-link">Start Lab</a>
        </div>

        <div class="lab-card">
            <div class="lab-type reflect">REFLECT</div>
            <h3>Error/Reflect-based SQL Injection</h3>
            <p>Use database errors and reflected output to extract information about the database structure and data.</p>
            <a href="reflect" class="lab-link">Start Lab</a>
        </div>

        <div class="lab-card">
            <div class="lab-type boolean">BOOLEAN</div>
            <h3>Boolean-based Blind SQL Injection</h3>
            <p>Extract data character by character using true/false responses when the application doesn't return data directly.</p>
            <a href="boolean" class="lab-link">Start Lab</a>
        </div>

        <div class="lab-card">
            <div class="lab-type time">TIME</div>
            <h3>Time-based Blind SQL Injection</h3>
            <p>Use database delays to confirm conditions and extract data when no visible output is available.</p>
            <a href="time" class="lab-link">Start Lab</a>
        </div>
    </div>
</body>
</html>
