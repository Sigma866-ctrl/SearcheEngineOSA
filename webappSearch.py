from flask import Flask, render_template_string, request
import json
import zlib
import base64
import os

app = Flask(__name__)

ENCODED_DATA = "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"

authlog_data = json.loads(
    zlib.decompress(base64.b64decode(ENCODED_DATA)).decode("utf-8"))

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Quiz Search</title>
    <style>
        body {
            font-family: system-ui, sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            margin: 0;
            display: flex;
            justify-content: center;
        }
        .container {
            max-width: 600px;
            width: 100%;
            padding: 1rem;
        }
        h1 {
            text-align: center;
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        input[type="text"] {
            padding: 0.8rem;
            font-size: 1rem;
            border: 1px solid #444;
            background-color: #1e1e1e;
            color: #e0e0e0;
            border-radius: 6px;
        }
        button {
            padding: 0.8rem;
            font-size: 1rem;
            border: none;
            border-radius: 6px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .keyword-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
            margin-bottom: 1.5rem;
        }
        .keyword-buttons button {
            background-color: #333;
            border: 1px solid #666;
            color: #fff;
            font-size: 0.9rem;
            padding: 0.5rem 0.8rem;
        }
        .question {
            background-color: #1e1e1e;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(255, 255, 255, 0.05);
        }
        ul {
            list-style: none;
            padding-left: 1rem;
        }
        .correct {
            color: #00ff88;
            font-weight: bold;
        }
    </style>
    <script>
        function insertKeyword(keyword) {
            const input = document.querySelector('input[name="keywords"]');
            if (!input.value.toLowerCase().includes(keyword.toLowerCase())) {
                input.value = input.value ? input.value + ", " + keyword : keyword;
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Quiz Search</h1>

        <form method="POST">
            <input type="text" name="keywords" placeholder="Enter keywords, separated by commas" required>
            <button type="submit">Search</button>
        </form>

        <div class="keyword-buttons">
        <button type="button" onclick="insertKeyword(\'.nvram\')">.nvram</button>
<button type="button" onclick="insertKeyword(\'.vmdk\')">.vmdk</button>
<button type="button" onclick="insertKeyword(\'.vmss\')">.vmss</button>
<button type="button" onclick="insertKeyword(\'.vmx\')">.vmx</button>
<button type="button" onclick="insertKeyword(\'.vswp\')">.vswp</button>
<button type="button" onclick="insertKeyword(\'/etc/shadow\')">/etc/shadow</button>
<button type="button" onclick="insertKeyword(\'AMI\')">AMI</button>
<button type="button" onclick="insertKeyword(\'AWS\')">AWS</button>
<button type="button" onclick="insertKeyword(\'CER\')">CER</button>
<button type="button" onclick="insertKeyword(\'CIM\')">CIM</button>
<button type="button" onclick="insertKeyword(\'CVE\')">CVE</button>
<button type="button" onclick="insertKeyword(\'DynamoDB\')">DynamoDB</button>
<button type="button" onclick="insertKeyword(\'ENI\')">ENI</button>
<button type="button" onclick="insertKeyword(\'ESXi\')">ESXi</button>
<button type="button" onclick="insertKeyword(\'HBA\')">HBA</button>
<button type="button" onclick="insertKeyword(\'IAM\')">IAM</button>
<button type="button" onclick="insertKeyword(\'Kerberos\')">Kerberos</button>
<button type="button" onclick="insertKeyword(\'LDAP\')">LDAP</button>
<button type="button" onclick="insertKeyword(\'LUN\')">LUN</button>
<button type="button" onclick="insertKeyword(\'MFA\')">MFA</button>
<button type="button" onclick="insertKeyword(\'NAS\')">NAS</button>
<button type="button" onclick="insertKeyword(\'NTLM\')">NTLM</button>
<button type="button" onclick="insertKeyword(\'OLAP\')">OLAP</button>
<button type="button" onclick="insertKeyword(\'OLTP\')">OLTP</button>
<button type="button" onclick="insertKeyword(\'RAID\')">RAID</button>
<button type="button" onclick="insertKeyword(\'Redshift\')">Redshift</button>
<button type="button" onclick="insertKeyword(\'S3\')">S3</button>
<button type="button" onclick="insertKeyword(\'SAN\')">SAN</button>
<button type="button" onclick="insertKeyword(\'SP\')">SP</button>
<button type="button" onclick="insertKeyword(\'SSH\')">SSH</button>
<button type="button" onclick="insertKeyword(\'SSO\')">SSO</button>
<button type="button" onclick="insertKeyword(\'TLS/SSL\')">TLS/SSL</button>
<button type="button" onclick="insertKeyword(\'VMFS\')">VMFS</button>
<button type="button" onclick="insertKeyword(\'VPC\')">VPC</button>
<button type="button" onclick="insertKeyword(\'clef/valeur\')">clef/valeur</button>
<button type="button" onclick="insertKeyword(\'vMotion\')">vMotion</button>
<button type="button" onclick="insertKeyword(\'vSAN\')">vSAN</button>
<button type="button" onclick="insertKeyword(\'vSphere\')">vSphere</button>

        {% if results %}
            <h2>Results</h2>
            {% for res in results %}
                <div class="question">
                    <strong>Q:</strong> {{ res['question'] }}
                    <ul>
                        {% for a in res['answers'] %}
                            <li class="{{ 'correct' if a['isCorrect'] else '' }}">
                                {{ a['letter'] }}) {{ a['text'] }}
                                {% if a['isCorrect'] %}(correct){% endif %}
                            </li>
                        {% endfor %}
                    </ul>
                </div>
            {% endfor %}
        {% elif searched %}
            <p>No matching questions found.</p>
        {% endif %}
    </div>
</body>
</html>
"""


def search_questions(keywords):
    keywords = [kw.strip().lower() for kw in keywords]
    results = []
    for q in authlog_data:
        if all(kw in q["question"].lower() for kw in keywords):
            results.append({
                "question": q["question"],
                "answers": q["answers"]
            })
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    searched = False
    if request.method == "POST":
        keywords = request.form.get("keywords", "").split(",")
        raw_results = search_questions(keywords)
        # Add letters and correct flags
        for r in raw_results:
            for i, a in enumerate(r["answers"]):
                a["letter"] = chr(65 + i)
        results = raw_results
        searched = True
    return render_template_string(TEMPLATE, results=results, searched=searched)


if __name__ == "__main__":
    if __name__ == "__main__":
        app.run(host="0.0.0.0",
                port=int(os.environ.get("PORT", 5000)),
                debug=True)
