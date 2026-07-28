import os
import requests

token = os.getenv('8889490346:AAFn2ZmNNG6B1jzcyneXf7GGYIyiqprp01g')
chat_id = os.getenv('5953644501')

print("--- DIAGNOSTIC TEST ---")
print(f"Did Python find the Bot Token? : {'✅ YES' if token else '❌ NO (It is empty)'}")
print(f"Did Python find the Chat ID?   : {'✅ YES' if chat_id else '❌ NO (It is empty)'}")
print("-----------------------")

if token and chat_id:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": "✅ <b>SUCCESS!</b>", "parse_mode": "HTML"}
    response = requests.post(url, json=payload)
    print(f"Telegram Server Response: {response.text}")
else:
    print("🚨 ERROR: The script stopped because the secrets are not reaching Python.")
    print("Please check your daily_scrape.yml file to ensure the 'env:' section is there.")
