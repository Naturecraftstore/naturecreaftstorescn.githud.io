import sqlite3
fashion_products = [
        ("H001", "Formal Shirt", 599, "Men's Cotton Rich Formal Shirt", "⭐ 4.2",'size-H001', "images3/fr1a.jpg"),
        ("H002", "Cotton Jacket", 749.99, "Premium men bomber jacket", "⭐ 4.6",'size-H002', "images3/ja.jpg"),
        ("H003", "Printed Half Sleeve Shirt", 499.99, "Printed half sleeve shirt", "⭐ 4.5",'size-H003', "images3/sa.jpg"),
        ("H004", "Cargo Pant", 749, "Cotton cargo pants", "⭐ 4.5",'size-H004', "images3/pa.jpg"),
        ("H005", "Hoodie for Men", 599, "Stylish hoodie sweatshirt", "⭐ 4.4",'size-H005', "images3/pu1.jpg"),
        ("H006", "Ethnic Wear Kurta Pajama Set", 649, "Traditional kurta pajama", "⭐ 4.7",'size-H006', "images3/kua.jpg"),
        ("H007", "Dhoti Set", 1299, "Traditional dhoti set", "⭐ 4.4",'size-H007', "images3/dhoti1.jpg"),
        ("H008", "Sweatshirts", 599, "Wool blend sweatshirt", "⭐ 4.4",'size-H008', "images3/sweatshirt2.jpg"),
        ("H009", "Men's Formal Shirt", 499, "Slim fit formal shirt", "⭐ 4.6",'size-H009', "images3/shirt1.jpg"),
        ("H010", "Flip Pocket Jeans", 799, "Loose fit jeans", "⭐ 4.6",'size-H010', "images3/pant3.jpg"),
        ('H011','Men T Shirt',467,'Soft, breathable 100% cotton fil-a-fil fabric with subtle texture.','⭐ 4.4 ','size-H011','images3/image1a.jpg'),
        ('H012','Men T Shirt',550,'Elegant mens kurta pajama crafted from soft','⭐ 4.7 ','size-H012','images3/image2a.jpg'),
        ('H013','Men T Shirt',600,'cotton fil-a-fil fabric with subtle texture.','⭐ 4.5 ','size-H013','images3/image3a.jpg'),
        ('H0014','Mens Cotton Dhoti',800,'Cotton Cargo Pants for Men','⭐4.6','size-H014','images3/image4a.jpg'),
        ('H015','Mens Cotton Dhoti',1000,'Compact sling bag','⭐ 4.8 ','size-H015','images3/image5a.jpg'),
        ('H016','Kurta-Pajama', 1500,'Elegant mens kurta pajama crafted from soft','⭐ 4.2','size-H016','images3/image6a.jpg'),
        ('H017','Kurta-Pajama', 2500,'family functions, and ethnic occasions.','⭐ 4.2 ','size-H017','images3/image7a.jpg'),
        ('H018','Mens short kurta', 1500,'breathable fabric for all-day comfort.','⭐ 4.6 ','size-H018','images3/image8a.jpg'),
        ('H019','Mens short kurta',1200,'Perfect for festivals, weddings, family functions .','⭐4.6','size-H019','images3/image9a.jpg'),
        ('H020','Mens Jeans Shirt',800,'Premium quality fabric.','⭐4.6','size-H020','images3/image10a.jpg')
    ]



def insert_products():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # PRODUCTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        price REAL,
        description TEXT,
        rating TEXT,
        category TEXT
    )
    """)

    # PRODUCT IMAGES TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS product_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT,
        image TEXT,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    for p in fashion_products:
        product_id, name, price, desc, rating, category, images = p

        cur.execute("""
        INSERT OR IGNORE INTO products
        (id, name, price, description, rating, category)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (product_id, name, price, desc, rating, category))

        for img in images:
            cur.execute("""
            INSERT INTO product_images (product_id, image)
            VALUES (?, ?)
            """, (product_id, img))

    conn.commit()
    conn.close()
    print("✅ Fashion products inserted successfully!")

if __name__ == "__main__":
    insert_products()
