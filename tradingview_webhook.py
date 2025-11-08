from flask import Flask, request, jsonify
from datetime import datetime
import os
import requests

app = Flask(__name__)

# 🔧 CONFIGURACIÓN TELEGRAM
TELEGRAM_BOT_TOKEN = "8496743597:AAHNJbQj77ysRnSKhCyWOC8-2TsvG-7D_sM"
TELEGRAM_CHAT_ID = "274526913"  

def enviar_mensaje_telegram(texto):
    """Envía un mensaje a tu chat de Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": texto, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Error al enviar mensaje a Telegram: {e}")

@app.route('/')
def home():
    return "🚀 Webhook activo. Usa /webhook para recibir alertas."

@app.route('/webhook', methods=['POST'])
def tradingview_webhook():
    data = request.json
    print(f"\n🔔 [{datetime.now()}] Alerta recibida:")
    print(data)

    # Guarda en archivo local
    with open("alerts_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {data}\n")

    # Mensaje formateado para Telegram
    mensaje = (
        f"📈 <b>Alerta TradingView</b>\n"
        f"<b>Ticker:</b> {data.get('ticker')}\n"
        f"<b>Precio:</b> {data.get('price')}\n"
        f"<b>Mensaje:</b> {data.get('alert') or data.get('message', '(sin mensaje)')}\n"
        f"<b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    enviar_mensaje_telegram(mensaje)
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

