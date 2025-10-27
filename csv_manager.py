import csv
import os
from datetime import datetime
import random
import json

# Path file CSV
CSV_PRODUCTS = 'data/products.csv'
CSV_CARTS = 'data/carts.csv'
CSV_ORDERS = 'data/orders.csv'

# ==================== HELPER FUNCTIONS ====================
def read_csv(file_path):
    """Baca data dari CSV"""
    if not os.path.exists(file_path):
        return []
    
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def write_csv(file_path, data, fieldnames):
    """Tulis data ke CSV"""
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_to_csv(file_path, row, fieldnames):
    """Tambah data baru ke CSV"""
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)

# ==================== PRODUCT FUNCTIONS ====================
def get_all_products():
    """Ambil semua produk"""
    return read_csv(CSV_PRODUCTS)

def get_product_by_id(product_id):
    """Cari produk by ID"""
    products = get_all_products()
    for product in products:
        if product['id'] == str(product_id):
            return product
    return None

def add_to_cart(user_wa, product_id, quantity=1):
    """Tambah item ke keranjang"""
    product = get_product_by_id(product_id)
    if not product:
        return False, "❌ Produk tidak ditemukan"
    
    carts = read_csv(CSV_CARTS)
    
    # Cek apakah produk sudah ada di cart
    for cart in carts:
        if cart['user_wa'] == user_wa and cart['product_id'] == str(product_id):
            new_quantity = int(cart['quantity']) + quantity
            cart['quantity'] = str(new_quantity)
            write_csv(CSV_CARTS, carts, ['user_wa', 'product_id', 'product_name', 'quantity', 'price'])
            return True, f"✅ {product['name']} ditambahkan ke keranjang (Total: {new_quantity})"
    
    # Jika belum ada, tambah item baru
    new_cart_item = {
        'user_wa': user_wa,
        'product_id': str(product_id),
        'product_name': product['name'],
        'quantity': str(quantity),
        'price': product['price']
    }
    
    append_to_csv(CSV_CARTS, new_cart_item, ['user_wa', 'product_id', 'product_name', 'quantity', 'price'])
    return True, f"✅ {product['name']} ditambahkan ke keranjang!"

def get_user_cart(user_wa):
    """Ambil keranjang user"""
    carts = read_csv(CSV_CARTS)
    return [cart for cart in carts if cart['user_wa'] == user_wa]

def remove_from_cart(user_wa, product_id):
    """Hapus item dari keranjang"""
    carts = read_csv(CSV_CARTS)
    updated_carts = [cart for cart in carts if not (cart['user_wa'] == user_wa and cart['product_id'] == str(product_id))]
    
    if len(updated_carts) < len(carts):
        write_csv(CSV_CARTS, updated_carts, ['user_wa', 'product_id', 'product_name', 'quantity', 'price'])
        return True, "✅ Item dihapus dari keranjang"
    return False, "❌ Item tidak ditemukan di keranjang"

def clear_user_cart(user_wa):
    """Kosongkan keranjang user"""
    carts = read_csv(CSV_CARTS)
    updated_carts = [cart for cart in carts if cart['user_wa'] != user_wa]
    write_csv(CSV_CARTS, updated_carts, ['user_wa', 'product_id', 'product_name', 'quantity', 'price'])
    return True

def create_order(user_wa, cart_items, total_amount):
    """Buat pesanan baru"""
    order_id = f"ORD{random.randint(1000, 9999)}"
    
    order_data = {
        'order_id': order_id,
        'user_wa': user_wa,
        'products': json.dumps(cart_items),
        'total_amount': str(total_amount),
        'status': 'pending',
        'timestamp': datetime.now().isoformat()
    }
    
    append_to_csv(CSV_ORDERS, order_data, ['order_id', 'user_wa', 'products', 'total_amount', 'status', 'timestamp'])
    return order_id