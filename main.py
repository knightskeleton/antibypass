from flask import Flask, request, redirect, render_template_string
import hashlib
import os

app = Flask(__name__)

# Secret key for generating tokens
SECRET_KEY = "KNIGHTSKULLISADMIN"

# Function to validate token
def is_valid_token(url, token):
    expected_token = hashlib.sha256((url + SECRET_KEY).encode()).hexdigest()
    return expected_token == token

# Countdown HTML template
COUNTDOWN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Redirecting...</title>
    <script>
        let timeLeft = 3;
        function countdown() {
            if (timeLeft > 0) {
                document.getElementById("countdown").innerHTML = timeLeft;
                timeLeft--;
                setTimeout(countdown, 1000);
            } else {
                window.location.href = "{{ final_url }}";
            }
        }
        window.onload = countdown;
    </script>
</head>
<body>
    <h2>Redirecting in <span id="countdown">3</span> seconds...</h2>
</body>
</html>
"""

@app.route('/redirect')
def process_redirect():
    url = request.args.get('url')
    token = request.args.get('token')

    if not url or not token:
        return "Invalid request", 400

    if not is_valid_token(url, token):
        return "Bypass detected! Access denied.", 403

    return render_template_string(COUNTDOWN_HTML, final_url=url)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
