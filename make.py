from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash, jsonify,
)
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from datetime import datetime, timedelta, date

import random

# ================= APP =================
app = Flask(__name__)
app.secret_key = "naturecraft_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.secret_key = "supersecretkey"

DB_PATH = "users.db"

# ================= DATABASE =================
def get_db():
    db = sqlite3.connect("users.db")
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db = sqlite3.connect(DB_PATH)


    # USERS
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            phone TEXT,
            email TEXT UNIQUE,
            dob TEXT,
            gender TEXT,
            password TEXT
        )
    """)

    # PRODUCTS
    db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            description TEXT,
            benefits TEXT,
            rating TEXT,
            category TEXT
        )
    """)

    # HANDMADE & ORGANIC (optional)
    db.execute("""
        CREATE TABLE IF NOT EXISTS handmade (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            description TEXT,
            benefits TEXT,
            rating TEXT,
            category TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS organic (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            description TEXT,
            benefits TEXT,
            rating TEXT,
            category TEXT
        )
    """)

    # PRODUCT IMAGES
    db.execute("""
        CREATE TABLE IF NOT EXISTS product_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            image TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    # CART
    db.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id TEXT,
            name TEXT,
            price REAL,
            image TEXT,
            qty INTEGER
        )
    """)

    # Orders table
    db.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    user_id INTEGER,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    district TEXT,
    state TEXT NOT NULL,
    pincode TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT DEFAULT 'PLACED',
    created_at TEXT NOT NULL
)
""")


    # Order items table
    db.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        image TEXT,
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )
    """)

    db.commit()
    db.close()


def get_current_order_status(order):
    """
    Determine current status based on created_at.
    0-20 min: PLACED
    20-40 min: SHIPPED
    40+ min: DELIVERED
    """
    if order["status"] == "CANCELLED":
        return "CANCELLED"

    # Convert string to datetime
    created_at = datetime.strptime(order["created_at"], "%Y-%m-%d %H:%M:%S")
    now = datetime.utcnow()

    if now >= created_at + timedelta(minutes=4):
        return "DELIVERED"
    elif now >= created_at + timedelta(minutes=2):
        return "SHIPPED"
    else:
        return "PLACED"

init_db()

# ================= BASIC PAGES =================
@app.route("/")
@app.route("/home")
def home():
    
    return render_template("home.html")

@app.route("/handmade")
def handmade():
    db = get_db()
    # This is the line where 'handmade' is assigned
    handmade = db.execute("SELECT * FROM handmade").fetchall()
    db.close()
    
    # You MUST pass the variable to the template to use it and clear the error
    return render_template("handmade.html", handmade=handmade)

@app.route("/organic")
def organic():
    db = get_db()
    items = db.execute("SELECT * FROM organic").fetchall()
    db.close()
    return render_template("organic.html", organic=items)


@app.route("/products")
def products():
    db = get_db()
    items = db.execute("SELECT * FROM products").fetchall()
    db.close()
    return render_template("products.html", products=items)




@app.route("/about")
def about():
    return render_template("about.html")

# ================= UNIVERSAL PRODUCT DETAIL =================
@app.route("/organic/<product_id>")
def organic_detail(product_id):
    db = get_db()

    # Fetch the product (case-insensitive)
    product = db.execute(
        "SELECT * FROM products WHERE (id)=?",
        (product_id.upper(),)
    ).fetchone()

    if not product:
        db.close()
        return "Product not found", 404

    # Fetch all images for this product
    images = db.execute(
        "SELECT image FROM product_images WHERE (product_id)=?",
        (product_id.upper(),)
    ).fetchall()
    db.close()

    return render_template(
        "organic_detail.html",
        product=product,
        images=[img["image"] for img in images]
    )

@app.route("/handmade/<product_id>")
def handmade_detail(product_id):
    db = get_db()

    # Fetch the product (case-insensitive)
    product = db.execute(
        "SELECT * FROM products WHERE (id)=?",
        (product_id.upper(),)
    ).fetchone()

    if not product:
        db.close()
        return "Product not found", 404

    # Fetch all images for this product
    images = db.execute(
        "SELECT image FROM product_images WHERE (product_id)=?",
        (product_id.upper(),)
    ).fetchall()
    db.close()

    # Pass 'product' here to clear the Ruff error and use it in your HTML
    return render_template(
        "handmade_detail.html",
        product=product,
        product_id=product_id, # This helps your JS filtering logic
        images=[img["image"] for img in images]
    )


@app.route("/product2/<product_id>")
def product2_detail(product_id):
    db = get_db()

    # Fetch the product (case-insensitive)
    product = db.execute(
        "SELECT * FROM products WHERE UPPER(id)=?",
        (product_id.upper(),)
    ).fetchone()

    if not product:
        db.close()
        return "Product not found", 404

    # Fetch all images for this product
    images = db.execute(
        "SELECT image FROM product_images WHERE UPPER(product_id)=?",
        (product_id.upper(),)
    ).fetchall()
    db.close()

    return render_template(
        "product2_detail.html",
        product=product,
        images=[img["image"] for img in images]
    )

# ================= CART =================
@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("cart.html")

@app.route("/cart-data")
def cart_data():
    if "user_id" not in session:
        return jsonify({"items": []})
    db = get_db()
    items = db.execute("SELECT * FROM cart WHERE user_id=?", (session["user_id"],)).fetchall()
    db.close()
    return jsonify({"items": [dict(i) for i in items]})

@app.route("/update-cart", methods=["POST"])
def update_cart():
    if "user_id" not in session:
        return jsonify({"success": False}), 401
    
    data = request.get_json()
    product_id = data.get("product_id")
    action = data.get("action")

    db = get_db()
    if action == "add":
        db.execute("UPDATE cart SET qty = qty + 1 WHERE user_id=? AND product_id=?", 
                   (session["user_id"], product_id))
    elif action == "subtract":
        # Prevents quantity from going below 1
        db.execute("UPDATE cart SET qty = MAX(1, qty - 1) WHERE user_id=? AND product_id=?", 
                   (session["user_id"], product_id))
    
    db.commit()
    db.close()
    return jsonify({"success": True})

@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    if "user_id" not in session:
        return jsonify({"success": False}), 401
    
    data = request.get_json()
    db = get_db()
    db.execute("DELETE FROM cart WHERE user_id=? AND product_id=?", 
               (session["user_id"], data.get("product_id")))
    db.commit()
    db.close()
    return jsonify({"success": True})

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    if "user_id" not in session:
        return jsonify({"error": "login required"}), 401
    data = request.get_json()
    db = get_db()
    item = db.execute(
        "SELECT * FROM cart WHERE user_id=? AND product_id=?",
        (session["user_id"], data["product_id"])
    ).fetchone()
    if item:
        db.execute("UPDATE cart SET qty = qty + 1 WHERE id=?", (item["id"],))
    else:
        db.execute("""
            INSERT INTO cart (user_id, product_id, name, price, image, qty)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (session["user_id"], data["product_id"], data["name"], data["price"], data["image"]))
    db.commit()
    db.close()
    return jsonify({"success": True})

@app.route("/buy-now", methods=["POST"])
def buy_now():
    if "user_id" not in session:
        return jsonify({"error": "login required"}), 401
    data = request.get_json()
    db = get_db()
    db.execute("DELETE FROM cart WHERE user_id=?", (session["user_id"],))
    db.execute("""
        INSERT INTO cart (user_id, product_id, name, price, image, qty)
        VALUES (?, ?, ?, ?, ?, 1)
    """, (session["user_id"], data["product_id"], data["name"], data["price"], data["image"]))
    db.commit()
    db.close()
    return jsonify({"success": True})

# ================= PAYMENT =================
@app.route("/payment")
def payment():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    items = db.execute(
        "SELECT * FROM cart WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()
    db.close()

    if not items:
        flash("Your cart is empty!")
        return redirect(url_for("cart"))

    total = sum(i["price"] * i["qty"] for i in items)
    return render_template("payment.html", items=items, total=total)


# --------------------- PLACE ORDER ---------------------
@app.route("/place-order", methods=["POST"])
def place_order():
    try:
        if not request.is_json:
            return jsonify({"success": False, "error": "Request must be JSON"}), 415

        data = request.get_json()

        # Required fields
        name = data.get("name")
        mobile = data.get("mobile")
        address = data.get("address")
        city = data.get("city")
        district = data.get("district", "")
        state = data.get("state")
        pincode = data.get("pincode")
        items = data.get("items", [])

        if not all([name, mobile, address, city, state, pincode, items]):
            return jsonify({"success": False, "error": "Missing fields"}), 400

        # Generate unique order ID
        order_id = "NCS" + str(random.randint(10000000, 99999999))

        # Total amount
        total = sum(item["price"] * item["quantity"] for item in items)

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Insert order
        cur.execute("""
    INSERT INTO orders 
    (order_id, user_id, name, mobile, address, city, district, state, pincode, total, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PLACED', ?)
""", (
    order_id,
    session["user_id"],
    name,
    mobile,
    address,
    city,
    district,
    state,
    pincode,
    total,
    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
))

        # Insert order items
        for item in items:
            cur.execute("""
                INSERT INTO order_items (order_id, name, price, quantity, image)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, item["name"], item["price"], item["quantity"], item.get("image", "")))

        conn.commit()
        conn.close()

        session["last_order_id"] = order_id

        return jsonify({"success": True, "order_id": order_id})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/order-confirmation/<order_id>")
def order_confirmation(order_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get order details
    cur.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cur.fetchone()
    if not order:
        conn.close()
        return "Order not found", 404

    # Get order items
    cur.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    items = cur.fetchall()
    conn.close()

    return render_template("order_confirmation.html",
                           order=order,
                           items=items)

@app.route("/api/order-items/<order_id>")
def api_order_items(order_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    items = [dict(row) for row in cur.fetchall()]
    conn.close()

    return jsonify({"items": items})


@app.route("/order-history")
def order_history():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    db = get_db()
    orders = db.execute("""
        SELECT * FROM orders
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()

    history = []
    for o in orders:
        # Determine current status
        current_status = get_current_order_status(o)

        # Update DB if needed
        if o["status"] != current_status:
            db.execute("UPDATE orders SET status=? WHERE order_id=?", 
                       (current_status, o["order_id"]))
            db.commit()

        items = db.execute("SELECT * FROM order_items WHERE order_id=?", 
                           (o["order_id"],)).fetchall()

        history.append({
            "order_id": o["order_id"],
            "created_at": o["created_at"],
            "total": o["total"],
            "status": current_status,
            "order_items": [dict(i) for i in items]
        })

    db.close()
    return render_template("order_history.html", history=history)

# ---------------------- Example buttons handling (optional) ----------------------
@app.route("/cancel-order/<order_id>", methods=["POST"])
def cancel_order(order_id):
    db = get_db()
    order = db.execute("SELECT * FROM orders WHERE order_id=?", (order_id,)).fetchone()
    if not order:
        db.close()
        return jsonify({"success": False, "error": "Order not found"})

    # Prevent cancelling delivered orders
    if get_current_order_status(order) == "DELIVERED":
        db.close()
        return jsonify({"success": False, "error": "Cannot cancel delivered order"})

    db.execute("UPDATE orders SET status='CANCELLED' WHERE order_id=?", (order_id,))
    db.commit()
    db.close()
    return jsonify({"success": True})


@app.route("/track-order/<order_id>")
def track_order(order_id):
    # Placeholder: you can implement tracking logic here
    db = get_db()
    cur = db.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,))
    status = cur.fetchone()["status"]
    return f"Order {order_id} status: {status}"



# ================= AUTH =================


# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        dob = request.form.get("dob", "")
        gender = request.form.get("gender", "")
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        # ---- VALIDATIONS ----
        if len(username) < 3:
            flash("Username must be at least 3 characters")
            return redirect(url_for("signup"))

        if not phone.isdigit() or len(phone) != 10:
            flash("Invalid phone number")
            return redirect(url_for("signup"))

        if password != confirm:
            flash("Passwords do not match")
            return redirect(url_for("signup"))

        # Age check ≥ 13
        dob_date = date.fromisoformat(dob)
        today = date.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        if age < 13:
            flash("You must be at least 13 years old")
            return redirect(url_for("signup"))

        # Hash password
        hashed_password = generate_password_hash(password)

        conn = get_db()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            flash("Email already registered")
            conn.close()
            return redirect(url_for("signup"))

        # Insert user
        cursor.execute("""
            INSERT INTO users (username, phone, email, dob, gender, password)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, phone, email, dob, gender, hashed_password))
        conn.commit()
        conn.close()

        flash("Registration successful! Please login.")
        return redirect(url_for("login"))

    return render_template("signup.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            flash("Email not registered ❌")
            return redirect(url_for("login"))

        if not check_password_hash(user["password"], password):
            flash("Invalid password ❌")
            return redirect(url_for("login"))

        # SUCCESS → set session
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash(f"Welcome, {user['username']} ✅")
        return redirect(url_for("home"))

    return render_template("login.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("about"))

# ================= LOGIN REQUIRED DECORATOR =================


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()
        if not user:
            flash("Email not registered", "error")
            return redirect(url_for("forgot_password"))
        session["reset_user"] = email
        return redirect(url_for("reset_password"))
    return render_template("forgot_password.html")

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if "reset_user" not in session:
        flash("Session expired. Try again.", "error")
        return redirect(url_for("forgot_password"))
    if request.method == "POST":
        password = request.form.get("password")
        db = get_db()
        db.execute(
            "UPDATE users SET password=? WHERE email=?",
            (generate_password_hash(password), session["reset_user"])
        )
        db.commit()
        session.pop("reset_user")
        flash("Password reset successful. Login now.", "success")
        return redirect(url_for("login"))
    return render_template("reset_password.html")

@app.route("/account")
def account():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    user = db.execute(
        "SELECT username, email, phone, dob, gender FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()
    db.close()
    return render_template("account.html", user=user)

@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    db = sqlite3.connect("users.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    if request.method == "POST":
        username = request.form.get("username").strip()
        phone = request.form.get("phone").strip()
        dob = request.form.get("dob")
        gender = request.form.get("gender")

        # Basic validation
        if len(username) < 3:
            flash("Username must be at least 3 characters")
            return redirect(url_for("edit_profile"))

        if not phone.isdigit() or len(phone) != 10:
            flash("Invalid phone number")
            return redirect(url_for("edit_profile"))

        # ✅ UPDATE USER
        cursor.execute("""
            UPDATE users
            SET username=?, phone=?, dob=?, gender=?
            WHERE id=?
        """, (username, phone, dob, gender, session["user_id"]))

        db.commit()
        db.close()

        flash("Profile updated successfully ✅")
        return redirect(url_for("account"))

    # GET → fetch current data
    cursor.execute(
        "SELECT username, phone, email, dob, gender FROM users WHERE id=?",
        (session["user_id"],)
    )
    user = cursor.fetchone()
    db.close()

    return render_template("edit_profile.html", user=user)

   
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        db = sqlite3.connect("users.db")
        cursor = db.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE id=?",
            (session["user_id"],)
        )
        user = cursor.fetchone()

        # ❌ Wrong current password
        if not user or not check_password_hash(user[0], current_password):
            db.close()
            flash("Enter current password correctly ", "error")
            return redirect(url_for("change_password"))

        # ❌ New password validation
        if len(new_password) < 6:
            db.close()
            flash("New password must be at least 6 characters ", "error")
            return redirect(url_for("change_password"))

        if new_password != confirm_password:
            db.close()
            flash("New passwords do not match ", "error")
            return redirect(url_for("change_password"))

        # ✅ Update password
        hashed_password = generate_password_hash(new_password)
        cursor.execute(
            "UPDATE users SET password=? WHERE id=?",
            (hashed_password, session["user_id"])
        )

        db.commit()
        db.close()

        flash("Password updated successfully ✅", "success")
        return redirect(url_for("account"))

    return render_template("change_password.html")


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
