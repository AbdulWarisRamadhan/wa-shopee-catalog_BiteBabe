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
    return """
    <html>
        <head><title>WA Shopee Catalog</title></head>
        <body>
            <h1>🚀 WA Shopee Catalog System is Running!</h1>
            <p><a href="/admin/products">Admin Products</a></p>
            <p><a href="/webhook">Webhook</a></p>
            <p>System ready for WhatsApp Business API</p>
        </body>
    </html>
    """

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

@app.route('/admin/products/add', methods=['POST'])
def admin_add_product():
    """Tambah produk baru via API"""
    from csv_manager import add_product
    data = request.json
    
    product = add_product(
        name=data['name'],
        price=data['price'],
        description=data['description'],
        image_url=data.get('image_url', ''),
        category=data['category'],
        stock=data['stock']
    )
    return jsonify({'success': True, 'product': product})

from datetime import datetime
# Health check untuk cloud
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'message': 'WA Shopee Catalog is running!',
        'environment_variables': {
            'whatsapp_token_loaded': bool(os.getenv('WHATSAPP_TOKEN')),
            'phone_number_loaded': bool(os.getenv('PHONE_NUMBER_ID')),
            'verify_token_loaded': bool(os.getenv('VERIFY_TOKEN'))
        }
    })
if __name__ == '__main__':
    # Untuk cloud, pakai port dari environment variable
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Starting WA Shopee Catalog System...")
    print(f"📱 Server: http://localhost:{port}")
    print("🔗 Webhook: /webhook")
    print("👨‍💼 Admin: /admin/products")
    app.run(host='0.0.0.0', port=port, debug=False)
