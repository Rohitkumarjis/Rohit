
import requests
import json
import time

# ==============================
# CONFIGURATION
# ==============================
BOT_TOKEN = "8712118205:AAHLN2u395qcj84n1C--6xoH3fWxlELUpM4"  # <-- PUT YOUR TELEGRAM BOT TOKEN HERE
API_URL = "https://astha-9vd8.onrender.com/tapi-4faabef4f8287eaf9020e5ff00dff1ff?phone="    # <-- PUT YOUR EXTERNAL API URL HERE

# Dummy HTTPS Server (for reference only)
DUMMY_SERVER = "https://example.com"

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ==============================
# SEND MESSAGE FUNCTION
# ==============================
def send_message(chat_id, text, reply_markup=None):
    url = BASE_URL + "/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    try:
        requests.post(url, data=payload)
    except:
        pass

# ==============================
# GET UPDATES FUNCTION
# ==============================
def get_updates(offset):
    url = BASE_URL + "/getUpdates"
    
    params = {
        "timeout": 100,
        "offset": offset
    }

    try:
        response = requests.get(url, params=params)
        return response.json()
    except:
        return {}

# ==============================
# MAIN BOT LOOP
# ==============================
def main():
    offset = 0

    # Custom Keyboard
    keyboard = {
        "keyboard": [[{"text": "📱 Phone Lookup"}]],
        "resize_keyboard": True
    }

    while True:
        data = get_updates(offset)

        if "result" in data:
            for update in data["result"]:
                offset = update["update_id"] + 1

                if "message" not in update:
                    continue

                message = update["message"]
                chat_id = message["chat"]["id"]

                if "text" not in message:
                    continue

                text = message["text"].strip()

                # ==============================
                # /start command
                # ==============================
                if text == "/start":
                    send_message(
                        chat_id,
                        "👋 Welcome!\n\nUse the button below to lookup phone details.",
                        reply_markup=keyboard
                    )

                # ==============================
                # Phone Lookup Button
                # ==============================
                elif text == "📱 Phone Lookup":
                    send_message(chat_id, "📞 Send 10 digit mobile number:")

                # ==============================
                # Handle Phone Number Input
                # ==============================
                elif text.isdigit() and len(text) == 10:
                    try:
                        api_call = f"{API_URL}?number={text}"
                        response = requests.get(api_call)
                        result = response.json()

                        formatted = json.dumps(result, indent=4)

                        send_message(chat_id, f"<pre>{formatted}</pre>")

                    except:
                        send_message(chat_id, "⚠️ API Error. Try again later.")

                # ==============================
                # Invalid Input
                # ==============================
                else:
                    send_message(chat_id, "❌ Invalid input.\nPlease send a valid 10-digit mobile number.")

        time.sleep(1)


# ==============================
# RUN BOT
# ==============================
if __name__ == "__main__":
    main()
