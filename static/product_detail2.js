document.addEventListener("DOMContentLoaded", () => {
    // ================= SHOW SINGLE PRODUCT IF ID PROVIDED =================
    const pathParts = window.location.pathname.split('/');
    let productId = pathParts[pathParts.length - 1];

    // Fallback to query parameter if path doesn't yield an ID
    if (!productId || productId.includes('handmade_detail') || productId === '') {
        const urlParams = new URLSearchParams(window.location.search);
        productId = urlParams.get('product_id');
    }

    // Filter display: show only the matching product box
    if (productId) {
        document.querySelectorAll('.product-box').forEach(box => {
            box.style.display = box.id === productId ? 'flex' : 'none';
        });
    }

    // ================= UPDATE CART COUNT ON LOAD =================
    updateCartCount();
});

// ================= RESPONSIVE MENU TOGGLE =================
function toggleMenu() {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
}

// ================= IMAGE GALLERY SWITCH =================
function changeImage(productId, thumb) {
    const productContainer = document.getElementById(productId);
    if (!productContainer) return;

    const mainImg = productContainer.querySelector('.main-image') || document.getElementById(`main-${productId}`);
    if (mainImg) {
        mainImg.src = thumb.src;
    }

    // Update active thumbnail styling
    thumb.parentElement.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
    thumb.classList.add('active');
}

// ================= ADD TO CART =================
function addToCart(id, name, price, img, rating) {
    fetch('/add-to-cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: id, name: name, price: price, image: img })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showToast(`${name} added to cart!`);
            updateCartCount();
        } else {
            showToast(data.error || "Could not add to cart", true);
            if (data.error === "login required") window.location.href = "/login";
        }
    })
    .catch(err => console.error("Add to Cart Error:", err));
}

// ================= BUY NOW =================
function buyNow(id, name, price, img, rating) {
    fetch('/buy-now', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: id, name: name, price: price, image: img })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/payment";
        } else {
            window.location.href = "/login";
        }
    })
    .catch(err => console.error("Buy Now Error:", err));
}

// ================= UPDATE CART COUNT =================
function updateCartCount() {
    const countElem = document.getElementById('cart-count');
    if (countElem) {
        fetch('/cart-count')
            .then(res => res.json())
            .then(data => { countElem.innerText = data.count || 0; })
            .catch(err => console.error("Cart Count Error:", err));
    }
}

// ================= SIMPLE TOAST NOTIFICATION =================
function showToast(message, isError = false) {
    let toast = document.createElement('div');
    toast.className = `toast ${isError ? 'error' : ''}`;
    toast.innerText = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
