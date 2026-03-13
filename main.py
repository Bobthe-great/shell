import subprocess
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Simple HTML template with CSS for a "terminal" look
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Shell</title>
    <style>
        body { background-color: #121212; color: #00ff00; font-family: monospace; padding: 20px; }
        input { background: #222; color: #00ff00; border: 1px solid #444; width: 80%; padding: 10px; }
        button { padding: 10px; cursor: pointer; background: #333; color: white; border: none; }
        .output { background: #000; border: 1px solid #333; padding: 15px; margin-top: 20px; white-space: pre-wrap; min-height: 200px; }
    </style>
</head>
<body>
    <h2>Internal Shell Access</h2>
    <form method="POST">
        <span>$ </span>
        <input type="text" name="command" autofocus placeholder="ls -la">
        <button type="submit">Execute</button>
    </form>
    
    <div class="output">
        {% if output %}{{ output }}{% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        cmd = request.form.get("command")
        try:
            # shell=True allows pipe (|) and redirects (>)
            # stderr=subprocess.STDOUT merges errors into the main output
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            output = result
        except subprocess.CalledProcessError as e:
            output = f"Error: {e.output}"
        except Exception as e:
            output = f"Critical Exception: {str(e)}"
            
    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == "__main__":
    # WARNING: Do not set host="0.0.0.0" on a public network without a password!
    app.run(debug=True)
