import os
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

# --- TELEGRAM CONFIGURATION ---
# These pull securely from your GitHub Secrets
TELEGRAM_BOT_TOKEN = os.getenv('8889490346: AAFn2ZmNNG6B1jzcyneXf 7GGYIyiqprp01g')
TELEGRAM_CHAT_ID = os.getenv('-1003773374191')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def calculate_shein_india_price(mrp, current_price, coupon_percent, available_points):
    # 1. Apply Coupon
    price_after_coupon = current_price * (1 - (coupon_percent / 100))
    # 2. Points Deduction (Max 70% of current total on SHEIN)
    max_points_discount = price_after_coupon * 0.70
    # Assuming 1 Point = 1 INR
    actual_points_discount = min(available_points, max_points_discount)
    return price_after_coupon - actual_points_discount

def scrape_with_browser():
    # The real SHEIN India Flash Deals URL
    url = "https://www.sheinindia.in/c/flashdeals-5798-94911" 
    my_coupon_percent = 15
    my_points = 500

    print("Starting invisible browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Go to SHEIN and wait 5 seconds for JavaScript to load the products
        page.goto(url)
        time.sleep(5) 
        
        # Grab the fully loaded HTML
        html = page.content()
        browser.close()

    print("Page loaded! Searching for deals...")
    soup = BeautifulSoup(html, 'html.parser')
    
    # NOTE: Update these class names if SHEIN changes them in the future
    product_cards = soup.find_all('div', class_='product-list-item') 
    
    deals_found = False
    message = "🚨 <b>SHEIN DISCOUNT ALERT</b> 🚨\n\n"
    
    for card in product_cards:
        try:
            title = card.find('a', class_='product-title').text.strip()
            
            # Extract numbers from price strings
            mrp_text = card.find('del', class_='original-price').text.replace('₹', '').replace(',', '')
            sale_text = card.find('span', class_='sale-price').text.replace('₹', '').replace(',', '')
            
            mrp = float(mrp_text)
            current_price = float(sale_text)
            
            # Calculate base discount percentage
            discount_percent = ((mrp - current_price) / mrp) * 100
            
            # Target alert threshold (Set to 80 for normal use, 0 for a guaranteed test message)
            if discount_percent >= 0: 
                deals_found = True
                final_checkout_price = calculate_shein_india_price(mrp, current_price, my_coupon_percent, my_points)
                
                message += f"👗 <b>{title[:30]}...</b>\n"
                message += f"💰 MRP: ₹{mrp} | Sale: ₹{current_price}\n"
                message += f"🔥 Discount: <b>{discount_percent:.1f}% OFF</b>\n"
                message += f"💳 Final Price (Stacked): ₹{final_checkout_price:.2f}\n"
                message += "-------------------------\n"
        except AttributeError:
            # Skips cards that might be missing price data
            continue

    if deals_found:
        send_telegram_message(message)
        print("Message sent to Telegram!")
    else:
        print("No products met the target discount threshold today.")

if __name__ == "__main__":
    scrape_with_browser()
