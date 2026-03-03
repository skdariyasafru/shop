// ================= MODAL FUNCTIONS =================

function openLogin() {
    const modal = document.getElementById("loginModal");
    if (modal) modal.style.display = "block";
}

function closeLogin() {
    const modal = document.getElementById("loginModal");
    if (modal) modal.style.display = "none";
}

function openRegister() {
    const modal = document.getElementById("registerModal");
    if (modal) modal.style.display = "block";
}

function closeRegister() {
    const modal = document.getElementById("registerModal");
    if (modal) modal.style.display = "none";
}

function switchToRegister() {
    closeLogin();
    openRegister();
}

function switchToLogin() {
    closeRegister();
    openLogin();
}

// Auto open login
document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    if (params.get("login") === "1") {
        openLogin();
    }
});

// Close modal outside click
window.addEventListener("click", function (event) {
    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    if (loginModal && event.target === loginModal) closeLogin();
    if (registerModal && event.target === registerModal) closeRegister();
});
