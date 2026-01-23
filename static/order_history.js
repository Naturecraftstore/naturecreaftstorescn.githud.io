
  // ==============================
  // CONFIG (TIMINGS)
  // ==============================
  const SHIPPED_TIME = 20 * 60 * 1000;    // 2 minutes
  const DELIVERED_TIME = 20 * 60 * 1000;  // 2 minutes after shipped

  // ==============================
  // CANCEL ORDER
  // ==============================
  function cancelOrder(orderId) {
    if (!confirm("Are you sure you want to cancel this order?")) return;

    fetch(`/cancel-order/${orderId}`, { method: "POST" })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          alert("Order cancelled");
          location.reload();
        } else {
          alert("Failed to cancel order");
        }
      });
  }

  // ==============================
  // TRACK ORDER (TOGGLE TIMELINE)
  // ==============================
  function trackOrder(orderId) {
    const timeline = document.getElementById(`timeline-${orderId}`);
    if (!timeline) return;

    timeline.style.display =
      timeline.style.display === "none" || timeline.style.display === ""
        ? "flex"
        : "none";
  }

  // ==============================
  // AUTO STATUS FLOW
  // PLACED → SHIPPED → DELIVERED
  // ==============================
  document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".order-card").forEach(order => {

      const statusDiv = order.querySelector(".status");
      const orderId = order.id.replace("order-", "");
      const timeline = document.getElementById(`timeline-${orderId}`);
      if (!statusDiv || !timeline) return;

      const steps = timeline.querySelectorAll(".step");
      const status = statusDiv.innerText.trim();

      // Always mark Order Placed
      steps[0].classList.add("done");

      // --------------------------
      // IF PLACED → AUTO SHIPPED
      // --------------------------
      if (status === "PLACED") {

        setTimeout(() => {
          statusDiv.innerText = "SHIPPED";
          statusDiv.className = "status shipped";
          steps[1].classList.add("done");

          // After shipped → delivered
          setTimeout(() => {
            statusDiv.innerText = "DELIVERED";
            statusDiv.className = "status delivered";
            steps[2].classList.add("done");
          }, DELIVERED_TIME);

        }, SHIPPED_TIME);
      }

      // --------------------------
      // IF ALREADY SHIPPED
      // --------------------------
      if (status === "SHIPPED") {
        steps[1].classList.add("done");

        setTimeout(() => {
          statusDiv.innerText = "DELIVERED";
          statusDiv.className = "status delivered";
          steps[2].classList.add("done");
        }, DELIVERED_TIME);
      }

      // --------------------------
      // IF ALREADY DELIVERED
      // --------------------------
      if (status === "DELIVERED") {
        steps[1].classList.add("done");
        steps[2].classList.add("done");
      }

    });

  });

function trackOrder(orderId) {
    const timeline = document.getElementById(`timeline-${orderId}`);
    timeline.style.display =
        timeline.style.display === "none" || timeline.style.display === "" 
        ? "flex" 
        : "none";
}

function cancelOrder(orderId) {
    if (!confirm("Are you sure you want to cancel this order?")) return;

    fetch(`/cancel-order/${orderId}`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Order cancelled");
                location.reload();
            } else {
                alert(data.error || "Cannot cancel order");
            }
        });
}

