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
// add item
function addToCart(productId, button) {

    fetch("/add_to_cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id: productId })
    })
    .then(response => {
        if (response.status === 401) {
            openLogin();
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.status === "added") {

            // 🔥 Change button text
            button.innerText = "Added ✓";

            // 🔥 Disable button
            button.disabled = true;

            // 🔥 Change button color
            button.style.background = "#28a745";
            button.style.cursor = "not-allowed";
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}



//end item


window.onclick = function(event) {
    if (event.target == document.getElementById("loginModal")) {
        closeLogin();
    }
    if (event.target == document.getElementById("registerModal")) {
        closeRegister();
    }
};
