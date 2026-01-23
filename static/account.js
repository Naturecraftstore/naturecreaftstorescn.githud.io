document.addEventListener("DOMContentLoaded", function () {
    const logoutBtn = document.querySelector(".logout");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (e) {
            const confirmLogout = confirm("Are you sure you want to logout?");
            if (!confirmLogout) {
                e.preventDefault();
            }
        });
    }
});
