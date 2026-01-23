// ==================== MOBILE MENU TOGGLE ====================
function toggleMenu() {
    const navLinks = document.getElementById("navLinks");
    navLinks.classList.toggle("show");
}

// ==================== CART FUNCTIONS ====================

// Add item to cart
function addToCart(productId, name, price, image, rating) {
    const data = { product_id: productId, name, price, image, rating, qty: 1 };

    fetch("/add-to-cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // Remove if not needed
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("cart-count").textContent = data.cart_count;
            showAlert(`${name} has been added to your cart!`);
        } else {
            showAlert("Failed to add to cart. Please try again.");
        }
    })
    .catch(error => {
        console.error("Error adding to cart:", error);
        showAlert("An error occurred.");
    });
}

// Buy now - add to cart and redirect to payment page
function buyNow(productId, name, price, image, rating) {
    const data = { product_id: productId, name, price, image, rating, qty: 1 };

    fetch("/buy-now", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // Remove if not needed
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/payment"; // redirect to payment page
        } else {
            showAlert("Failed to proceed to payment. Please try again.");
        }
    })
    .catch(error => {
        console.error("Error on Buy Now:", error);
        showAlert("An error occurred.");
    });
}

// ==================== HELPER FUNCTIONS ====================

// Get CSRF token for Flask-WTF
function getCSRFToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}

// Simple alert wrapper (can later be replaced with toast)
function showAlert(message) {
    alert(message);
}

// ==================== INITIALIZE CART COUNT ====================
document.addEventListener("DOMContentLoaded", () => {
    // Fetch current cart count
    fetch("/cart-count")
        .then(response => response.json())
        .then(data => {
            if (data.cart_count !== undefined) {
                document.getElementById("cart-count").textContent = data.cart_count;
            }
        })
        .catch(error => console.error("Error fetching cart count:", error));

    // Optional: close mobile menu when clicking outside
    document.addEventListener("click", function(e) {
        const navLinks = document.getElementById("navLinks");
        const menuIcon = document.querySelector(".menu-icon");
        if (!navLinks.contains(e.target) && !menuIcon.contains(e.target)) {
            navLinks.classList.remove("show");
        }
    });
});
