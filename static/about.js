// Fade-in animation for feature boxes
const featureBoxes = document.querySelectorAll(".feature-box");

window.addEventListener("scroll", () => {
    featureBoxes.forEach(box => {
        const position = box.getBoundingClientRect().top;
        if (position < window.innerHeight - 50) {
            box.style.opacity = "1";
            box.style.transform = "translateY(0)";
        }
    });
});

// Initial hidden state
featureBoxes.forEach(box => {
    box.style.opacity = "0";
    box.style.transform = "translateY(20px)";
    box.style.transition = "0.8s ease";
});

// Gallery click
document.querySelectorAll(".gallery-container img").forEach(img => {
    img.addEventListener("click", () => {
        alert("This product belongs to Nature Craft Store!");
    });
});

// Navbar shadow
window.addEventListener("scroll", () => {
    const navbar = document.querySelector(".navbar");
    navbar.style.boxShadow =
        window.scrollY > 50
            ? "0 3px 15px rgba(0,0,0,0.2)"
            : "0 2px 10px rgba(0,0,0,0.1)";
});
