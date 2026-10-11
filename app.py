
from flask import Flask, render_template_string, request
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Generate sample network traffic data for demonstration
def generate_data():
    data = []
    labels = []

    for _ in range(1000):
        packet_rate = random.randint(1, 500)
        packet_size = random.randint(40, 1500)
        connections = random.randint(1, 100)

        # Synthetic rules for demonstration only
        if packet_rate > 300 and connections > 60:
            label = 1  # DoS-like traffic
        else:
            label = 0  # Normal-like traffic

        data.append([packet_rate, packet_size, connections])
        labels.append(label)

    return data, labels

X, y = generate_data()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI DoS Detection System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #101827;
            color: white;
            margin: 0;
            padding: 30px;
        }
        .container {
            max-width: 650px;
            margin: auto;
            background: #1d293b;
            padding: 30px;
            border-radius: 15px;
        }
        h1 { color: #38bdf8; text-align: center; }
        p { color: #cbd5e1; line-height: 1.6; }
        label { display: block; margin-top: 18px; }
        input {
            width: 100%;
            padding: 12px;
            margin-top: 8px;
            box-sizing: border-box;
            border-radius: 6px;
            border: 1px solid #475569;
        }
        button {
            width: 100%;
            padding: 13px;
            margin-top: 24px;
            background: #0284c7;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }
        .result {
            margin-top: 24px;
            padding: 18px;
            background: #334155;
            border-radius: 8px;
            text-align: center;
        }
        .note { font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI DoS Detection System</h1>
        <p>
            Enter sample network traffic values to demonstrate
            machine-learning-based traffic classification.
        </p>

        <form method="POST">
            <label>Packet Rate (packets per second)</label>
            <input type="number" name="packet_rate"
                   min="1" max="1000000" value="100" required>

            <label>Average Packet Size (bytes)</label>
            <input type="number" name="packet_size"
                   min="1" max="65535" value="500" required>

            <label>Number of Connections</label>
            <input type="number" name="connections"
                   min="1" max="1000000" value="20" required>

            <button type="submit">Analyze Traffic</button>
        </form>

        {% if result %}
        <div class="result">
            <h2>{{ result }}</h2>
            <p>{{ details }}</p>
        </div>
        {% endif %}

        <p class="note">
            Educational demo only. This uses synthetic data and is
            not validated for detecting real-world cyberattacks.
        </p>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    details = ""

    if request.method == "POST":
        try:
            packet_rate = int(request.form["packet_rate"])
            packet_size = int(request.form["packet_size"])
            connections = int(request.form["connections"])

            if not (
                1 <= packet_rate <= 1000000
                and 1 <= packet_size <= 65535
                and 1 <= connections <= 1000000
            ):
                raise ValueError("Values are outside the allowed range.")

            prediction = model.predict(
                [[packet_rate, packet_size, connections]]
            )[0]

            if prediction == 1:
                result = "DoS-like Traffic Pattern"
                details = (
                    "The sample model classified this input as "
                    "similar to its synthetic DoS examples."
                )
            else:
                result = "Normal-like Traffic Pattern"
                details = (
                    "The sample model classified this input as "
                    "similar to its synthetic normal examples."
                )

        except (ValueError, TypeError):
            result = "Invalid Input"
            details = "Please enter valid numeric values."

    return render_template_string(
        HTML_PAGE, result=result, details=details
    )

if __name__ == "__main__":
    app.run(debug=True)