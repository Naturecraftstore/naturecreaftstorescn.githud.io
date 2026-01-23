// ===============================
// Run AFTER page loads
// ===============================
document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("paymentForm");
    const payBtn = document.getElementById("payBtn");
    const msg = document.getElementById("msg");

    const cardBox = document.getElementById("cardBox");
    const upiBox = document.getElementById("upiBox");

    // Address fields
    const nameEl = document.getElementById("name");
    const mobileEl = document.getElementById("mobile");
    const addressEl = document.getElementById("address");
    const villageEl = document.getElementById("village");
    const mandalEl = document.getElementById("mandal");
    const pincodeEl = document.getElementById("pincode");
    const cityEl = document.getElementById("city");
    const districtEl = document.getElementById("district");
    const stateEl = document.getElementById("state");

    const fields = [nameEl, mobileEl, addressEl, villageEl, mandalEl, pincodeEl, cityEl, districtEl, stateEl];

    // ---------------- Payment method toggle ----------------
    window.showCard = () => {
        cardBox.style.display = "block";
        upiBox.style.display = "none";
    };
    window.showUPI = () => {
        cardBox.style.display = "none";
        upiBox.style.display = "block";
    };
    window.hideAll = () => {
        cardBox.style.display = "none";
        upiBox.style.display = "none";
    };

    // ---------------- Enable Pay button ----------------
    fields.forEach(f => f.addEventListener("input", checkForm));

    function checkForm() {
        let valid = true;
        fields.forEach(f => {
            if (!f || f.value.trim() === "") valid = false;
        });
        payBtn.disabled = !valid;
    }

    // ---------------- Read cart items ----------------
    function getCartItems() {
        const items = [];
        document.querySelectorAll(".product-item").forEach(item => {
            const name = item.querySelector(".product-name").innerText.trim();
            const qty = parseInt(item.querySelector(".product-qty").innerText.replace("Qty:", "").trim());
            const total = parseFloat(item.querySelector(".product-price").innerText.replace("₹", "").trim());
            const price = total / qty;
            const image = item.querySelector("img").getAttribute("src").replace("/static/", "");

            items.push({ name, price, quantity: qty, image });
        });
        return items;
    }

    // ---------------- Submit order ----------------
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        msg.innerText = "";
        payBtn.disabled = true;

        const items = getCartItems();
        if (items.length === 0) {
            msg.innerText = "Your cart is empty";
            payBtn.disabled = false;
            return;
        }

        const data = {
            name: nameEl.value.trim(),
            mobile: mobileEl.value.trim(),
            address: `${addressEl.value}, ${villageEl.value}, ${mandalEl.value}`,
            city: cityEl.value.trim(),
            district: districtEl.value.trim(),
            state: stateEl.value.trim(),
            pincode: pincodeEl.value.trim(),
            items: items
        };

        try {
            const res = await fetch("/place-order", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.success) {
                window.location.href = `/order-confirmation/${result.order_id}`;
            } else {
                msg.innerText = result.error || "Payment failed";
                payBtn.disabled = false;
            }
        } catch (err) {
            msg.innerText = "Server error. Please try again.";
            payBtn.disabled = false;
        }
    });

});

// ---------------- Pincode autofill ----------------
function getAddress() {
    const pin = document.getElementById("pincode").value;
    if (pin.length !== 6) return;

    fetch(`https://api.postalpincode.in/pincode/${pin}`)
        .then(res => res.json())
        .then(data => {
            if (data[0].Status === "Success") {
                document.getElementById("city").value = data[0].PostOffice[0].Block;
                document.getElementById("district").value = data[0].PostOffice[0].District;
                document.getElementById("state").value = data[0].PostOffice[0].State;
                // Recheck form after autofill
                document.querySelectorAll("#paymentForm input, #paymentForm textarea").forEach(f => f.dispatchEvent(new Event('input')));
            }
        });
}
