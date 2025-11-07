from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Webhook activo. Usa /webhook para recibir alertas."

@app.route('/webhook', methods=['POST'])
def tradingview_webhook():
    data = request.json

    print(f"\n🔔 [{datetime.now()}] Alerta recibida:")
    print(data)

    # Guarda las alertas en un archivo
    with open("alerts_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {data}\n")

    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
