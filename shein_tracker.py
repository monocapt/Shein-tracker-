import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv('8889490346:AAFn2ZmNNG6B1jzcyneXf7GGYIyiqprp01g')
TELEGRAM_CHAT_ID = os.getenv('-1003773374191')

def test_telegram():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": "✅ <b>SUCCESS!</b> Your Telegram bot is perfectly connected to GitHub Actions!", 
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_telegram()
