function openLogin() {
    document.getElementById("loginModal").style.display = "block";
}

function closeLogin() {
    document.getElementById("loginModal").style.display = "none";
}

function openRegister() {
    document.getElementById("registerModal").style.display = "block";
}

function closeRegister() {
    document.getElementById("registerModal").style.display = "none";
}

function switchToRegister() {
    closeLogin();
    openRegister();
}

function switchToLogin() {
    closeRegister();
    openLogin();
}

window.onclick = function(event) {
    if (event.target == document.getElementById("loginModal")) {
        closeLogin();
    }
    if (event.target == document.getElementById("registerModal")) {
        closeRegister();
    }
};
