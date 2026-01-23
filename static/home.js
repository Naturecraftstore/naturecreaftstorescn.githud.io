document.addEventListener("DOMContentLoaded", () => {

    /* ===== HERO SLIDER ===== */
    let slideIndex = 0;
    const slides = document.querySelectorAll(".slide");

    function showSlides() {
        slides.forEach(slide => {
            slide.style.display = "none";
        });

        slideIndex++;
        if (slideIndex > slides.length) slideIndex = 1;

        if (slides[slideIndex - 1]) {
            slides[slideIndex - 1].style.display = "block";
        }
    }

    if (slides.length > 0) {
        showSlides();
        setInterval(showSlides, 3000);
    }

    /* ===== CART COUNT (FRONTEND ONLY) ===== */
    function updateCartCount() {
        let cart = JSON.parse(localStorage.getItem("cart")) || [];
        let cartCount = document.getElementById("cart-count");

        if (cartCount) {
            cartCount.innerText = cart.length;
        }
    }

    updateCartCount();

    /* ===== IMAGE CLICK / TOUCH EFFECT ===== */
    document.querySelectorAll("img").forEach(img => {
        img.addEventListener("touchstart", () => {
            img.classList.add("highlight");
        });

        img.addEventListener("touchend", () => {
            img.classList.remove("highlight");
        });

        img.addEventListener("click", () => {
            img.classList.add("highlight");
            setTimeout(() => img.classList.remove("highlight"), 300);
        });
    });

});

/* ===== MOBILE MENU ===== */
function toggleMenu() {
    document.getElementById("navLinks").classList.toggle("active");
}

/* ===== CLOSE MENU AFTER CLICK (MOBILE UX) ===== */
document.addEventListener("click", (e) => {
    const navLinks = document.getElementById("navLinks");
    const menuIcon = document.querySelector(".menu-icon");

    if (!navLinks || !menuIcon) return;

    if (!navLinks.contains(e.target) && !menuIcon.contains(e.target)) {
        navLinks.classList.remove("active");
    }
});
