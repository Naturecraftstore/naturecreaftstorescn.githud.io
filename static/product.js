// ==================== SERVER-SIDE CART ====================

// Add to Cart
function addToCart(productId, name, price, image, rating) {
    let size = prompt("Enter size (S, M, L) or leave blank if N/A:") || null;
    if (size) size = size.toUpperCase();

    // Send product data to Flask route
    fetch("/add-to-cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // if you are using Flask-WTF
        },
        body: JSON.stringify({
            product_id: productId,
            name: name,
            price: price,
            image: image,
            rating: rating,
            size: size,
            qty: 1
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`${name} added to cart!`);
            document.getElementById("cart-count").textContent = data.cart_count;
        } else {
            alert("Failed to add to cart.");
        }
    })
    .catch(err => console.error(err));
}

// Buy Now
function buyNow(productId, name, price, image, rating) {
    let size = prompt("Enter size (S, M, L) or leave blank if N/A:") || null;
    if (size) size = size.toUpperCase();

    // Send product data to Flask route
    fetch("/buy-now", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // if using Flask-WTF
        },
        body: JSON.stringify({
            product_id: productId,
            name: name,
            price: price,
            image: image,
            rating: rating,
            size: size,
            qty: 1
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to cart page
            window.location.href = "/cart";
        } else {
            alert("Failed to proceed to buy now.");
        }
    })
    .catch(err => console.error(err));
}

// Helper function for CSRF token if Flask-WTF is used
function getCSRFToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}
