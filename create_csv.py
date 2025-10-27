import csv
import os

def create_csv_files():
    # Buat folder data jika belum ada
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Data produk sample
    products_data = [
        ['id', 'name', 'price', 'description', 'image_url', 'category', 'stock'],
        [1, 'iPhone 14 Pro', 15999000, 'iPhone 14 Pro 128GB Garansi Internasional', 'https://example.com/iphone14.jpg', 'Smartphone', 10],
        [2, 'Samsung Galaxy S23', 12999000, 'Samsung Galaxy S23 256GB Garansi Resmi', 'https://example.com/s23.jpg', 'Smartphone', 15],
        [3, 'MacBook Air M2', 19999000, 'MacBook Air M2 8GB/256GB Garansi Apple', 'https://example.com/macbook.jpg', 'Laptop', 5],
        [4, 'Nike Air Force 1', 1599000, 'Sepatu Nike Air Force 1 Original', 'https://example.com/nike.jpg', 'Fashion', 20],
        [5, 'Smart TV 55 inch', 5499000, 'Smart TV LED 55 inch 4K UHD', 'https://example.com/tv.jpg', 'Electronics', 8]
    ]
    
    # Tulis products.csv
    with open('data/products.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(products_data)
    
    # Buat carts.csv (header saja)
    with open('data/carts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['user_wa', 'product_id', 'product_name', 'quantity', 'price'])
    
    # Buat orders.csv (header saja)
    with open('data/orders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['order_id', 'user_wa', 'products', 'total_amount', 'status', 'timestamp'])
    
    print("✅ File CSV berhasil dibuat!")
    print("📁 products.csv - Data produk")
    print("📁 carts.csv - Data keranjang")
    print("📁 orders.csv - Data pesanan")

if __name__ == '__main__':
    create_csv_files()
