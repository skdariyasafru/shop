/* ================= AUTH FUNCTIONS ================= */

function openLogin() {
    const modal = document.getElementById("loginModal");
    if (modal) modal.style.display = "flex";
}

function closeLogin() {
    const modal = document.getElementById("loginModal");
    if (modal) modal.style.display = "none";
}

function openRegister() {
    const modal = document.getElementById("registerModal");
    if (modal) modal.style.display = "flex";
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


/* ================= REFERRAL SYSTEM ================= */

function setReferralCode() {
    const params = new URLSearchParams(window.location.search);
    const ref = params.get("ref");

    if (ref) {
        const input = document.getElementById("referral_code");
        if (input) {
            input.value = ref;
        }
    }
}


/* ================= AUTO OPEN ================= */

document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);

    // ✅ Open login popup
    if (params.get("login") === "1") {
        openLogin();
    }

    // ✅ Open register popup if referral
    if (params.get("ref")) {
        openRegister();
    }

    // ✅ Set referral code
    setReferralCode();
});


/* ================= CLOSE OUTSIDE ================= */

window.addEventListener("click", function (event) {
    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    if (loginModal && event.target === loginModal) closeLogin();
    if (registerModal && event.target === registerModal) closeRegister();
});
