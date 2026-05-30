/* ================= AUTH FUNCTIONS ================= */

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

window.openLogin = openLogin;
window.closeLogin = closeLogin;
window.openRegister = openRegister;
window.closeRegister = closeRegister;

window.addEventListener("click", function (event) {
    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    if (event.target === loginModal) closeLogin();
    if (event.target === registerModal) closeRegister();
});
