import requests
from bs4 import BeautifulSoup

# --- TELEGRAM CONFIGURATION ---
TELEGRAM_BOT_TOKEN = '8889490346: AAFn2ZmNNG6B1jzcyneXf 7GGYIyiqprp01g'
TELEGRAM_CHAT_ID = '-1003773374191'

def send_telegram_message(message):
    """Sends a formatted HTML message to your Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML" # Allows bolding and formatting in the message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def calculate_shein_india_price(mrp, current_price, coupon_percent, available_points):
    """Calculates final price after stacking a coupon and max points."""
    price_after_coupon = current_price * (1 - (coupon_percent / 100))
    max_points_discount = price_after_coupon * 0.70
    user_points_inr = available_points * 1 
    actual_points_discount = min(user_points_inr, max_points_discount)
    return price_after_coupon - actual_points_discount

def scrape_and_notify_highest_discounts(url, my_coupon_percent, my_points):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # NOTE: Update these class names based on SHEIN's live website structure
        product_cards = soup.find_all('div', class_='product-list-item') 
        
        deals_found = False
        message = "🚨 <b>SHEIN 80%+ DISCOUNT ALERT</b> 🚨\n\n"
        
        for card in product_cards:
            try:
                title = card.find('a', class_='product-title').text.strip()
                mrp_text = card.find('del', class_='original-price').text.replace('₹', '').replace(',', '')
                sale_text = card.find('span', class_='sale-price').text.replace('₹', '').replace(',', '')
                
                mrp = float(mrp_text)
                current_price = float(sale_text)
                
                # Calculate discount percentage
                discount_percent = ((mrp - current_price) / mrp) * 100
                
                # Check if it meets the 80% threshold
                if discount_percent >= 0:
                    deals_found = True
                    final_checkout_price = calculate_shein_india_price(mrp, current_price, my_coupon_percent, my_points)
                    
                    message += f"👗 <b>{title[:30]}...</b>\n"
                    message += f"💰 MRP: ₹{mrp} | Sale: ₹{current_price}\n"
                    message += f"🔥 Discount: <b>{discount_percent:.1f}% OFF</b>\n"
                    message += f"💳 Final Price (Stacked): ₹{final_checkout_price:.2f}\n"
                    message += "-------------------------\n"
                    
            except AttributeError:
                continue

        if deals_found:
            send_telegram_message(message)
            print("High discount found! Alert sent to Telegram.")
        else:
            print("No 80%+ deals found today.")
            
    except Exception as e:
        print(f"Error scraping data: {e}")

# --- RUN THE SCRIPT ---
target_url = "https://www.shein.in/flash-sale-page-url-here" 
scrape_and_notify_highest_discounts(target_url, my_coupon_percent=15, my_points=500)

