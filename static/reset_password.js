
document.getElementById("resetForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const newPassword = document.getElementById("newPassword").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  if (newPassword !== confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  const res = await fetch("/reset-password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: newPassword })
  });

  const data = await res.json();

  if (data.success) {
    alert("Password reset successful!");
    window.location.href = "/login";   // ✅ LOGIN PAGE
  } else {
    alert(data.error || "Reset failed");
  }
});
function togglePassword(fieldId) {
    const input = document.getElementById(fieldId);
    const toggle = input.nextElementSibling;

    if (input.type === "password") {
        input.type = "text";
        toggle.textContent = "Hide";
    } else {
        input.type = "password";
        toggle.textContent = "Show";
    }
}
