let captcha = "";

/* ===== GENERATE CAPTCHA ===== */
function generateCaptcha() {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    captcha = "";

    for (let i = 0; i < 6; i++) {
        captcha += chars.charAt(Math.floor(Math.random() * chars.length));
    }

    document.getElementById("captchaText").innerText = captcha;
}

/* ===== SHOW / HIDE PASSWORD ===== */
function togglePassword() {
    const password = document.getElementById("password");
    const toggle = document.querySelector(".toggle-password");

    if (password.type === "password") {
        password.type = "text";
        toggle.textContent = "Hide";
    } else {
        password.type = "password";
        toggle.textContent = "Show";
    }
}

/* ===== ON PAGE LOAD ===== */
document.addEventListener("DOMContentLoaded", function () {

    generateCaptcha();

    const form = document.getElementById("loginForm");

    form.addEventListener("submit", function (e) {

        const captchaInput = document.getElementById("captchaInput").value.trim();

        if (captchaInput === "") {
            e.preventDefault();
            alert("Please enter captcha ❗");
            return;
        }

        if (captchaInput !== captcha) {
            e.preventDefault();
            alert("Invalid captcha ❌");
            generateCaptcha(); // regenerate captcha
            document.getElementById("captchaInput").value = "";
            return;
        }

        // ✅ Captcha correct → Flask will handle login
    });
});
