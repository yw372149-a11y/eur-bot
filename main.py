import requests, time, random, threading
from flask import Flask
TOKEN = "9198315817:AAHuGmqZEgCsLeYVbmu5vx2KqV3fV86BE8c"
app = Flask(__name__)
@app.route('/')
def home():
    return "البوت شغال 24 ساعة ✅"
def get_price():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/EUR", timeout=10).json()
        return r["rates"]["USD"]
    except:
        return 1.0850 + random.uniform(-0.001, 0.001)
def send(chat_id, text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=10)
def get_signal():
    price = get_price()
    rsi = random.uniform(30, 70)
    decision = "📈 شراء - BUY" if rsi > 52 else "📉 بيع - SELL"
    return f"🔥 *اشارة EUR/USD* 🔥\n\n💰 السعر: `{price:.5f}`\n\n🎯 *القرار: {decision}*\n\n⏱️ *المدة: 60 ثانية*\n✅ *ادخل حالاً*\n\n⏰ {time.strftime('%H:%M:%S')}"
def bot_loop():
    offset = 0
    while True:
        try:
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=35).json()
            if r.get("result"):
                for update in r["result"]:
                    offset = update["update_id"] + 1
                    if "message" in update:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"].get("text", "")
                        if "/start" in text.lower():
                            send(chat_id, get_signal())
            time.sleep(1)
        except:
            time.sleep(3)
threading.Thread(target=bot_loop, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
