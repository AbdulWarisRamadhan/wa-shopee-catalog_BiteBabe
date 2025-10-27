import requests
import os
from dotenv import load_dotenv
from csv_manager import *

# Load environment variables
load_dotenv()

WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

class WhatsAppIntegration:
    def __init__(self):
        self.token = WHATSAPP_TOKEN
        self.phone_number_id = PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
    
    def send_message(self, to, message):
        """Kirim pesan teks ke WhatsApp"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            print(f"📤 Message sent to {to}")
            return response.json()
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return None

def send_welcome_message(user_wa):
    """Kirim pesan welcome"""
    wa = WhatsAppIntegration()
    
    message = """🛍️ *SELAMAT DATANG DI TOKO KAMI!*

*MENU UTAMA:*
📋 PRODUK - Lihat katalog produk
🛒 KERANJANG - Lihat keranjang belanja  
💳 CHECKOUT - Selesaikan pesanan

*CARA BELANJA:*
1. Ketik PRODUK untuk lihat katalog
2. Ketik BELI [nomor] untuk tambah ke keranjang
3. Ketik KERANJANG untuk lihat cart
4. Ketik CHECKOUT untuk selesaikan pesanan

Contoh: BELI 1 untuk beli produk nomor 1"""
    
    wa.send_message(user_wa, message)

def send_catalog(user_wa):
    """Kirim katalog produk"""
    wa = WhatsAppIntegration()
    products = get_all_products()
    
    catalog_text = "🏪 *KATALOG PRODUK*\n\n"
    
    for product in products:
        price = int(float(product['price']))
        catalog_text += f"*{product['id']}. {product['name']}*\n"
        catalog_text += f"💰 Rp {price:,}\n"
        catalog_text += f"📦 Stok: {product['stock']}\n"
        catalog_text += f"🛒 Ketik BELI {product['id']} untuk beli\n\n"
    
    wa.send_message(user_wa, catalog_text)

def send_cart(user_wa):
    """Kirim isi keranjang"""
    wa = WhatsAppIntegration()
    cart_items = get_user_cart(user_wa)
    
    if not cart_items:
        wa.send_message(user_wa, "🛒 Keranjang Anda masih kosong")
        return
    
    total = 0
    cart_text = "🛒 *KERANJANG BELANJA*\n\n"
    
    for item in cart_items:
        subtotal = float(item['price']) * int(item['quantity'])
        total += subtotal
        cart_text += f"• {item['product_name']}\n"
        cart_text += f"  Jumlah: {item['quantity']} x Rp {int(float(item['price'])):,}\n"
        cart_text += f"  Subtotal: Rp {int(subtotal):,}\n\n"
    
    cart_text += f"💰 TOTAL: Rp {int(total):,}\n\n"
    cart_text += "Ketik CHECKOUT untuk memesan"
    
    wa.send_message(user_wa, cart_text)

def process_checkout(user_wa):
    """Proses checkout"""
    wa = WhatsAppIntegration()
    cart_items = get_user_cart(user_wa)
    
    if not cart_items:
        wa.send_message(user_wa, "❌ Keranjang Anda kosong!")
        return
    
    # Hitung total
    total = sum(float(item['price']) * int(item['quantity']) for item in cart_items)
    
    # Buat pesanan
    order_id = create_order(user_wa, cart_items, total)
    
    # Kosongkan keranjang
    clear_user_cart(user_wa)
    
    # Kirim konfirmasi
    confirmation_msg = f"""✅ *PESANAN BERHASIL!*

Order ID: {order_id}
Total: Rp {int(total):,}

Admin akan menghubungi Anda."""
    
    wa.send_message(user_wa, confirmation_msg)

def handle_text_message(user_wa, text):
    """Handle pesan text dari user"""
    text = text.lower().strip()
    
    if text in ['hai', 'halo', 'hi', 'hello', 'menu']:
        send_welcome_message(user_wa)
    
    elif text in ['produk', 'katalog']:
        send_catalog(user_wa)
    
    elif text in ['keranjang', 'cart']:
        send_cart(user_wa)
    
    elif text.startswith('beli '):
        try:
            product_id = text.split(' ')[1]
            success, message = add_to_cart(user_wa, product_id)
            wa = WhatsAppIntegration()
            wa.send_message(user_wa, message)
        except:
            wa = WhatsAppIntegration()
            wa.send_message(user_wa, "❌ Format: BELI [nomor]")
    
    elif text == 'checkout':
        process_checkout(user_wa)
    
    else:
        wa = WhatsAppIntegration()
        wa.send_message(user_wa, "Ketik MENU untuk bantuan")
