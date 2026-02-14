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
function addToCart(productId) {
    fetch("/add_to_cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id: productId })
    })
    .then(response => {
        if (response.status === 401) {
            openLogin();  // 🔥 open popup instead of refresh
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.status === "added") {
            window.location.href = "/cart";
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

window.onclick = function(event) {
    if (event.target == document.getElementById("loginModal")) {
        closeLogin();
    }
    if (event.target == document.getElementById("registerModal")) {
        closeRegister();
    }
};
