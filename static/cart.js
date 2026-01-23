 function fetchCartData() {
            fetch('/cart-data')
                .then(res => res.json())
                .then(data => {
                    const list = document.getElementById('cart-items-list');
                    const summary = document.getElementById('cart-summary');
                    const totalSpan = document.getElementById('grand-total');
                    
                    if (data.items.length === 0) {
                        list.innerHTML = '<h3>Your cart is empty.</h3>';
                        summary.style.display = 'none';
                        return;
                    }

                    let total = 0;
                    list.innerHTML = '';
                    data.items.forEach(item => {
                        total += (item.price * item.qty);
                        list.innerHTML += `
                            <div class="cart-item">
                                <img src="/static/${item.image}">
                                <div class="cart-details">
                                    <h4>${item.name}</h4>
                                    <p>Price: ₹${item.price}</p>
                                    <div class="qty-controls">
                                        <button class="qty-btn" onclick="updateQty('${item.product_id}', 'subtract')">-</button>
                                        <span>${item.qty}</span>
                                        <button class="qty-btn" onclick="updateQty('${item.product_id}', 'add')">+</button>
                                    </div>
                                </div>
                                <div class="item-actions">
                                    <p><strong>₹${(item.price * item.qty).toFixed(2)}</strong></p>
                                    <span class="remove-link" onclick="removeItem('${item.product_id}')">Remove</span>
                                </div>
                            </div>`;
                    });
                    totalSpan.innerText = total.toFixed(2);
                    summary.style.display = 'block';
                });
        }

        function updateQty(productId, action) {
            fetch('/update-cart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ product_id: productId, action: action })
            }).then(() => fetchCartData());
        }

        function removeItem(productId) {
            fetch('/remove-from-cart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ product_id: productId })
            }).then(() => fetchCartData());
        }

        document.addEventListener('DOMContentLoaded', fetchCartData);
    function toggleMenu() {
    const nav = document.getElementById("navLinks");
    nav.classList.toggle("active");
}