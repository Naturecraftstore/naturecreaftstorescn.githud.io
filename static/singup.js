document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", (e) => {
    const username = form.username.value.trim();
    const phone = form.phone.value.trim();
    const email = form.email.value.trim();
    const password = form.password.value;
    const confirm = form.confirm.value;
    const dobValue = form.dob.value;

    // Username length
    if (username.length < 3) {
      alert("Username must be at least 3 characters long");
      e.preventDefault();
      return;
    }

    // Phone number validation (10 digits)
    if (!/^\d{10}$/.test(phone)) {
      alert("Please enter a valid 10-digit phone number");
      e.preventDefault();
      return;
    }

    // Email validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
      alert("Please enter a valid email address");
      e.preventDefault();
      return;
    }

    // Password length
    if (password.length < 6) {
      alert("Password must be at least 6 characters long");
      e.preventDefault();
      return;
    }

    // Password match
    if (password !== confirm) {
      alert("Passwords do not match");
      e.preventDefault();
      return;
    }

    // Age validation (minimum 13 years)
    const dob = new Date(dobValue);
    const today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    const monthDiff = today.getMonth() - dob.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
      age--;
    }

    if (age < 13) {
      alert("You must be at least 13 years old to register");
      e.preventDefault();
      return;
    }
  });
});
function togglePassword(inputId, toggleElement) {
    const input = document.getElementById(inputId);

    if (input.type === "password") {
        input.type = "text";
        toggleElement.textContent = "Hide";
    } else {
        input.type = "password";
        toggleElement.textContent = "Show";
    }
}
