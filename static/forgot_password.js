document.getElementById("forgotForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();

  if (!email) {
    alert("Please enter your email");
    return;
  }

  fetch("/forgot_password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert("Email verified! Please reset your password.");
      window.location.href = "/forgot_password";
    } else {
      alert(data.error || "Email not registered");
    }
  })
  .catch(() => {
    alert("Server error. Try again later.");
  });
});
