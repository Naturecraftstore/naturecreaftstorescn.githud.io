document.getElementById("changePasswordForm").addEventListener("submit", function (e) {
    const currentPassword = document.querySelector('input[name="current_password"]').value.trim();
    const newPassword = document.querySelector('input[name="new_password"]').value.trim();
    const confirmPassword = document.querySelector('input[name="confirm_password"]').value.trim();

    if (currentPassword === "") {
        alert("Enter current password ");
        e.preventDefault();
        return;
    }

    if (newPassword.length < 6) {
        alert("New password must be at least 6 characters ");
        e.preventDefault();
        return;
    }

    if (newPassword !== confirmPassword) {
        alert("New passwords do not match ");
        e.preventDefault();
        return;
    }
});
function togglePassword(el) {
    const input = el.previousElementSibling;
    if (input.type === "password") {
        input.type = "text";
        el.textContent = "👁️"; // eye-off icon
    } else {
        input.type = "password";
        el.textContent = "👁️"; // eye icon
    }
}
