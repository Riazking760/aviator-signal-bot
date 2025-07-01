from flask import Flask, render_template_string
import requests

app = Flask(__name__)

API_KEY = "5ce6f44076msh176fa1ea2b316fbp1f125djsnd0e35fa7fefd"
URL = "https://bet7k-aviator-api.p.rapidapi.com/bet7k-aviator-history"
HEADERS = {
    "x-rapidapi-host": "bet7k-aviator-api.p.rapidapi.com",
    "x-rapidapi-key": API_KEY
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Aviator Signal Bot</title>
    <style>
        body { font-family: Arial; background: #0f0f0f; color: white; text-align: center; padding: 50px; }
        .logo { width: 100px; margin-bottom: 20px; }
        .box { background: #1e1e1e; border-radius: 10px; padding: 20px; display: inline-block; }
        .signal { font-size: 24px; margin-top: 15px; font-weight: bold; }
        .green { color: #00ff88; }
        .red { color: #ff4c4c; }
    </style>
</head>
<body>
    <img class="logo" src="https://cdn-icons-png.flaticon.com/512/8209/8209853.png" alt="Aviator Logo">
    <div class="box">
        <h2>🎮 Aviator Signal Bot</h2>
        <p>Last 5 Multipliers: {{ multipliers }}</p>
        <div class="signal {{ color }}">{{ signal }}</div>
        <p>✅ Recommended: Cash out above <strong>{{ recommended }}x</strong></p>
    </div>
</body>
</html>
"""

def get_signal():
    try:
        res = requests.get(URL, headers=HEADERS)
        if res.status_code == 200:
            data = res.json()
            multipliers = [float(item['multiplier']) for item in data[:5]]
            low_count = sum(1 for m in multipliers if m < 2.0)

            if low_count >= 3:
                signal = "✅ BET NOW! Good Chance Coming!"
                color = "green"
                recommended = "2.0"
            else:
                signal = "⛔ WAIT! Too Risky"
                color = "red"
                recommended = "1.5"

            return signal, color, multipliers, recommended
        else:
            return "API Error", "red", [], "N/A"
    except Exception as e:
        return f"Error: {str(e)}", "red", [], "N/A"

@app.route("/")
def home():
    signal, color, multipliers, recommended = get_signal()
    return render_template_string(HTML_TEMPLATE,
                                  signal=signal,
                                  color=color,
                                  multipliers=multipliers,
                                  recommended=recommended)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


