from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from whatsapp_handler import handle_text_message

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Config
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

@app.route('/')
def home():
    return "🚀 WA Shopee Catalog System is Running!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Webhook untuk WhatsApp Business API"""
    
    # VERIFY WEBHOOK
    if request.method == 'GET':
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == VERIFY_TOKEN:
            print("✅ Webhook verified!")
            return challenge
        else:
            return 'Verification failed', 403
    
    # HANDLE INCOMING MESSAGES
    if request.method == 'POST':
        data = request.get_json()
        print("📩 Received webhook data")
        
        try:
            if data.get('object') == 'whatsapp_business_account':
                for entry in data.get('entry', []):
                    for change in entry.get('changes', []):
                        messages = change.get('value', {}).get('messages', [])
                        if messages:
                            message = messages[0]
                            user_wa = message['from']
                            message_type = message.get('type')
                            
                            if message_type == 'text':
                                text_body = message['text']['body']
                                print(f"💬 Message from {user_wa}: {text_body}")
                                handle_text_message(user_wa, text_body)
            
            return jsonify({'status': 'success'}), 200
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return jsonify({'status': 'error'}), 500

@app.route('/admin/products')
def admin_products():
    """Lihat semua produk"""
    from csv_manager import get_all_products
    products = get_all_products()
    return jsonify(products)

if __name__ == '__main__':
    print("🚀 Starting WA Shopee Catalog System...")
    print("📱 http://localhost:5000")
    app.run(debug=True, port=5000)