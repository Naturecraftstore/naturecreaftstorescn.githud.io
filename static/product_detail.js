/***********************
 IMAGE CHANGE
************************/
function changeImage(productId, thumb) {
    const mainImg = document.getElementById(`main-${productId}`);
    if (!mainImg) return;

    mainImg.src = thumb.src;

    const thumbs = thumb.parentElement.querySelectorAll('.thumb');
    thumbs.forEach(t => t.classList.remove('active'));
    thumb.classList.add('active');
}

/***********************
 SIZE SELECTION
************************/
function getSelectedSize(sizeGroupName) {
    const radios = document.getElementsByName(sizeGroupName);
    for (let r of radios) {
        if (r.checked) return r.value;
    }
    return null;
}

/***********************
 ADD TO CART (FLASK)
************************/
function addToCart(id, name, price, image, rating, sizeGroupName) {
    const size = getSelectedSize(sizeGroupName);
    if (!size) {
        alert("Please select a size");
        return;
    }

    fetch("/add_to_cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id,
            name,
            price,
            image,
            rating,
            size,
            quantity: 1
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            updateCartCount(data.cart_count);
            alert("Item added to cart!");
        } else {
            alert(data.message || "Error adding to cart");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Server error");
    });
}

/***********************
 BUY NOW (FLASK)
************************/
function buyNow(id, name, price, image, rating, sizeGroupName) {
    const size = getSelectedSize(sizeGroupName);
    if (!size) {
        alert("Please select a size");
        return;
    }

    fetch("/buy_now", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id,
            name,
            price,
            image,
            rating,
            size,
            quantity: 1
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/checkout";
        } else {
            alert(data.message || "Error");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Server error");
    });
}

/***********************
 CART COUNT
************************/
function updateCartCount(count) {
    const cartCount = document.getElementById("cart-count");
    if (cartCount) cartCount.textContent = count;
}

/***********************
 INITIAL CART COUNT LOAD
************************/
document.addEventListener("DOMContentLoaded", () => {
    fetch("/cart_count")
        .then(res => res.json())
        .then(data => updateCartCount(data.cart_count))
        .catch(() => {});
});
