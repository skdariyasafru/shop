// ================= LOGIN MODAL =================

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


// ================= ADD TO CART =================

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

        if (data && data.status === "added" && button) {

            button.innerText = "Added ✓";
            button.disabled = true;
            button.style.background = "#28a745";
            button.style.cursor = "not-allowed";
        }
    })
    .catch(error => {
        console.error("Cart Error:", error);
    });
}


// ================= LIVE SEARCH =================

document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");

    if (!searchInput) return;

    searchInput.addEventListener("keyup", function () {

        let query = this.value.trim();

        if (query.length < 1) {
            searchResults.innerHTML = "";
            searchResults.style.display = "none";
            return;
        }

        fetch(`/search?q=${query}`)
            .then(res => res.json())
            .then(data => {

                searchResults.innerHTML = "";

                if (data.length === 0) {
                    searchResults.style.display = "none";
                    return;
                }

                data.forEach(product => {

                    const item = document.createElement("a");

                    item.href = `/product/${product.id}`;
                    item.classList.add("search-item");

                    item.innerHTML = `
                        <img src="${product.image}" alt="${product.name}" width="40">
                        <div>
                            <h4>${product.name}</h4>
                            <p>₹${product.price}</p>
                        </div>
                    `;

                    searchResults.appendChild(item);
                });

                searchResults.style.display = "block";
            })
            .catch(error => {
                console.error("Search Error:", error);
            });
    });

    // Hide dropdown when clicking outside
    document.addEventListener("click", function(e) {
        if (!searchInput.contains(e.target) &&
            !searchResults.contains(e.target)) {
            searchResults.style.display = "none";
        }
    });
});


// ================= CLOSE MODALS OUTSIDE CLICK =================

window.onclick = function(event) {

    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    if (event.target === loginModal) {
        closeLogin();
    }

    if (event.target === registerModal) {
        closeRegister();
    }
};
