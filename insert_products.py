import sqlite3

DB_NAME = "users.db"

def ensure_image_column(cursor):
    """Check if 'image' column exists; if not, add it."""
    cursor.execute("PRAGMA table_info(products)")
    columns = [col[1] for col in cursor.fetchall()]
    if "image" not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN image TEXT")
        print("✅ 'image' column added to products table")

def insert_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ================= CREATE TABLE =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        price REAL,
        description TEXT,
        rating TEXT
    )
    """)

    # Ensure 'image' column exists
    ensure_image_column(cursor)

    # ================= HANDMADE PRODUCTS =================
    handmade_products = [
        ("P001", "Handmade Bag", 210, "Beautiful Handmade Bag", "⭐ 4.2", "images1/bag1.png"),
        ("P002", "Cotton Handmade Bag", 359.9, "Premium multicolour bag", "⭐ 4.6", "images1/bag4.jpg"),
        ("P003", "Purse", 299, "Handcrafted purse", "⭐ 4.5", "images1/purse3.webp"),
        ("P004", "Sling Bag", 249, "Traditional sling bag", "⭐ 4.6", "images1/sling bag6.webp"),
        ("P005", "Multicolour Purse", 349, "Eco-friendly jute purse", "⭐ 4.4", "images1/purse8.jpg"),
        ("P006", "Handmade Earring", 230, "Thread earring", "⭐ 4.4", "images1/earnings5.jpg"),
        ("P007", "Sling Bag", 467, "Eco-friendly sling bag", "⭐ 4.4", "images1/slingbag 7.jpg"),
        ("P008", "Jhumka", 798.9, "Multicolour jhumka", "⭐ 4.4", "images1/earning7.jpg"),
        ("P009", "Handmade Bangles", 249, "Decorative bangles", "⭐ 4.6", "images1/bangle5.jpg"),
        ("P010", "Bangle", 478, "Stylish bangle", "⭐ 4.3", "images1/bangle6.jpg"),
        ("P011", "Thread Bangle", 216.99, "Thread work bangle", "⭐ 4.8", "images1/bangle7.jpg"),
        ("P012", "Handmade Saree", 1199.99, "Traditional handcrafted saree", "⭐ 4.6", "images1/pattren1b.jpg"),
        ("P013", "Smooth Saree", 699.9, "Elegant handmade saree", "⭐ 4.1", "images1/pat6a.jpg"),
        ("P014", "Cotton Saree", 2110, "Soft cotton saree", "⭐ 4.2", "images1/pat 3a.jpg"),
        ("P015", "Modern Saree", 2299, "Elegant modern saree", "⭐ 4.7", "images1/pat5a.jpg"),
        ("P016", "Beats Sling Bag", 349, "Compact sling bag", "⭐ 4.6", "images1/sling bag3.jpg"),
    ]

    # ================= ORGANIC BEAUTY =================
    organic_products = [
        ("OB01", "Aloe Vera Soap", 199.99, "Natural aloe vera soap", "⭐ 4.2", "images2/AS1.png"),
        ("OB02", "Aloe Vera Shampoo", 320, "Herbal aloe shampoo", "⭐ 4.6", "images2/AS11.jpeg"),
        ("OB03", "Hibiscus Shampoo", 399, "Hibiscus hair care shampoo", "⭐ 4.4", "images2/HS1.png"),
        ("OB04", "Lavender Bliss Soap", 259, "Relaxing lavender soap", "⭐ 4.5", "images2/LS1.png"),
        ("OB05", "Meethi Seeds & Curry Leaves Hair Oil", 249, "Hair strengthening oil", "⭐ 4.4", "images2/mc1.jpeg"),
        ("OB06", "Rose Bliss Soap", 299, "Rose scented soap", "⭐ 4.3", "images2/RS1.jpeg"),
        ("OB07", "Turmeric Glow Soap", 349, "Turmeric glow soap", "⭐ 4.6", "images2/TS1.jpeg"),
        ("OB08", "Meethi Seeds & Rosemary Hair Oil", 699, "Hair growth oil", "⭐ 4.1", "images2/mr1.jpeg"),
        ("OB09", "Lemon Brightening Face Pack", 249, "Brightening face pack", "⭐ 4.4", "images2/l1.jpeg"),
        ("OB10", "Orange & Neem Face Pack", 399, "Acne control face pack", "⭐ 4.2", "images2/on1.jpeg"),
        ("OB11", "Onion Shampoo", 349, "Onion hair shampoo", "⭐ 4.2", "images2/OS1.jpeg"),
        ("OB12", "Rose Hair Oil", 429, "Rose infused hair oil", "⭐ 4.3", "images2/ro1.jpeg"),
        ("OB13", "Multani Mitti Face Pack", 399, "Clay face pack", "⭐ 4.1", "images2/mm1.jpeg"),
        ("OB14", "Rose Powder Face Pack", 349, "Natural rose powder", "⭐ 4.5", "images2/rp1.jpeg"),
        ("OB15", "Neem Shampoo", 199, "Neem herbal shampoo", "⭐ 4.3", "images2/NS1.png"),
    ]

    # ================= FASHION =================
    fashion_products = [
        ("H001", "Formal Shirt", 599, "Men's Cotton Rich Formal Shirt", "⭐ 4.2", "images3/fr1a.jpg"),
        ("H002", "Cotton Jacket", 749.99, "Premium men bomber jacket", "⭐ 4.6", "images3/ja.jpg"),
        ("H003", "Printed Half Sleeve Shirt", 499.99, "Printed half sleeve shirt", "⭐ 4.5", "images3/sa.jpg"),
        ("H004", "Cargo Pant", 749, "Cotton cargo pants", "⭐ 4.5", "images3/pa.jpg"),
        ("H005", "Hoodie for Men", 599, "Stylish hoodie sweatshirt", "⭐ 4.4", "images3/pu1.jpg"),
        ("H006", "Ethnic Wear Kurta Pajama Set", 649, "Traditional kurta pajama", "⭐ 4.7", "images3/kua.jpg"),
        ("H007", "Dhoti Set", 1299, "Traditional dhoti set", "⭐ 4.4", "images3/dhoti1.jpg"),
        ("H008", "Sweatshirts", 599, "Wool blend sweatshirt", "⭐ 4.4", "images3/sweatshirt2.jpg"),
        ("H009", "Men's Formal Shirt", 499, "Slim fit formal shirt", "⭐ 4.6", "images3/shirt1.jpg"),
        ("H010", "Flip Pocket Jeans", 799, "Loose fit jeans", "⭐ 4.6", "images3/pant3.jpg"),
         ('H011','Men T Shirt',467,'images3/image1a.jpg','Soft, breathable 100% cotton fil-a-fil fabric with subtle texture.','⭐ 4.4 '),
        ('H012','Men T Shirt',550,'images3/image2a.jpg','Elegant men’s kurta pajama crafted from soft','⭐ 4.7 '),
        ('H013','Men T Shirt',600,'images3/image3a.jpg','cotton fil-a-fil fabric with subtle texture.','⭐ 4.5 '),
        ('H0014','Mens Cotton Dhoti',800,'images3/image4a.jpg','Cotton Cargo Pants for Men','⭐4.5',),
        ('H015','Mens Cotton Dhoti',1000,'images3/image5a.jpg','Compact sling bag','⭐ 4.8 '),
        ('H016','Kurta–Pajama', 1500,'images3/image6a.jpg','Elegant men’s kurta pajama crafted from soft','⭐ 4.2'),
        ('H017','Kurta–Pajama', 2500,'images3/image7a.jpg','family functions, and ethnic occasions.','⭐ 4.2 '),
        ('H018','Men’s short kurta', 1500,'images3/image8a.jpg','breathable fabric for all-day comfort.','⭐ 4.6 '),
        ('H019','Men’s short kurta',1200,'images3/images10a.jpg','Perfect for festivals, weddings, family functions .','⭐4.6'),
        ('H020','Men’s Jeans Shirt',800,'images3/images10a.jpg','Premium quality fabric.','⭐4.6')
    ]

    # ================= INSERT =================
    cursor.executemany("""
    INSERT OR IGNORE INTO products
    (id, name, price, description, rating, image)
    VALUES (?, ?, ?, ?, ?, ?)
    """, handmade_products + organic_products + fashion_products)

    conn.commit()
    conn.close()

    print("✅ All products inserted successfully!")

if __name__ == "__main__":
    insert_products()
