<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boolean-based Blind SQL Injection</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .query-display { background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 15px 0; border-radius: 4px; font-family: monospace; white-space: pre-wrap; }
        .result-box { background-color: #e9ecef; border: 1px solid #ced4da; padding: 15px; margin: 15px 0; border-radius: 4px; }
        .error { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
        .success { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .false-result { background-color: #fff3cd; border: 1px solid #ffeaa7; color: #856404; }
        .back-link { display: inline-block; padding: 10px 20px; background-color: #6c757d; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        .result-indicator { font-size: 24px; font-weight: bold; text-align: center; padding: 20px; margin: 15px 0; border-radius: 8px; }
        .true-indicator { background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb; }
        .false-indicator { background-color: #f8d7da; color: #721c24; border: 2px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <a href="{{ route('sqli.index') }}" class="back-link">← Back</a>
        <h1>Boolean-based Blind SQL Injection</h1>

        <form method="GET" action="{{ route('sqli.boolean') }}">
            <div style="margin: 20px 0;">
                <label for="name"><strong>Name parameter:</strong></label>
                <input type="text" name="name" value="{{ $searchTerm }}" placeholder="Enter username" style="width: 400px; padding: 8px;">
                <button type="submit" style="padding: 8px 16px; margin-left: 10px;">Check</button>
            </div>
        </form>

        @if($query)
            <div class="query-display">{{ $query }}</div>
        @endif

        @if($error)
            <div class="result-box error"><strong>Error:</strong> {{ $error }}</div>
        @elseif($searchTerm !== null)
            @if($exists === true)
                <div class="result-indicator true-indicator">User exists</div>
            @elseif($exists === false)
                <div class="result-indicator false-indicator">User does not exist</div>
            @endif
        @endif
    </div>
</body>
</html>
