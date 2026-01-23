document.addEventListener("DOMContentLoaded", () => {
    const orderId = document.getElementById("orderId").dataset.orderId;
    const itemsContainer = document.getElementById("itemsContainer");
    const totalEl = document.getElementById("totalAmount");

    fetch(`/api/order-items/${orderId}`)
        .then(res => res.json())
        .then(data => {
            let total = 0;
            data.items.forEach(item => {
                const itemTotal = item.price * item.quantity;
                total += itemTotal;

                const div = document.createElement("div");
                div.className = "item";
                div.innerHTML = `
                    <img src="/static/${item.image}" alt="${item.name}">
                    <div>
                        <h4>${item.name}</h4>
                        <p>Qty: ${item.quantity}</p>
                        <p>Price: ${item.price}</p>
                        <p>Total: ${itemTotal}</p>
                    </div>
                `;
                itemsContainer.appendChild(div);
            });
            totalEl.innerText = `${total}`;
        });
});
