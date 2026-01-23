import sqlite3

conn = sqlite3.connect("users.db")
db = conn.cursor()

handmade_products = [
    ("P001","Handmade Bag",210,"Beautiful Handmade Bag","Eco-friendly, durable","⭐4.2","Bag"),
    ("P002","Cotton Handmade Bag",359.9,"Premium multicolour bag","Lightweight cotton","⭐4.6","Bag"),
    ("P003","Purse",299,"Handcrafted purse","Compact and stylish","⭐4.5","Purse"),
    ("P004","Sling Bag",249,"Traditional sling bag","Strong and spacious","⭐4.6","Bag"),
    ("P005","Multicolour Purse",349,"Eco-friendly jute purse","Light and durable","⭐4.4","Purse"),
    ("P006","Handmade Earring",230,"Thread earring","Handcrafted detail","⭐4.4","Jewellery"),
    ("P007","Sling Bag",467,"Eco-friendly sling bag","Strong and stylish","⭐4.4","Bag"),
    ("P008","Jhumka",798.9,"Multicolour jhumka","Beautiful design","⭐4.4","Jewellery"),
    ("P009","Handmade Bangles",249,"Decorative bangles","Traditional style","⭐4.6","Jewellery"),
    ("P010","Bangle",478,"Stylish bangle","Elegant look","⭐4.3","Jewellery"),
    ("P011","Thread Bangle",216.99,"Thread work bangle","Handmade craft","⭐4.8","Jewellery"),
    ("P012","Handmade Saree",1199.99,"Traditional handcrafted saree","Soft and vibrant","⭐4.6","Clothing"),
    ("P013","Smooth Saree",699.9,"Elegant handmade saree","Lightweight design","⭐4.1","Clothing"),
    ("P014","Cotton Saree",2110,"Soft cotton saree","Comfortable","⭐4.2","Clothing"),
    ("P015","Modern Saree",2299,"Elegant modern saree","Contemporary design","⭐4.7","Clothing"),
    ("P016","Beats Sling Bag",349,"Compact sling bag","Practical and trendy","⭐4.6","Bag")
]

for p in handmade_products:
    db.execute("""
        INSERT OR REPLACE INTO handmade
        (id, name, price, description, benefits, rating, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, p)

conn.commit()
conn.close()
print("Handmade products inserted successfully!")
