// ================= LOGIN MODAL =================

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


// ================= ADD TO CART =================

function addToCart(productId, button) {

    fetch("/add_to_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: productId })
    })
    .then(response => {
        if (response.status === 401) {
            openLogin();
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.status === "added" && button) {
            button.innerText = "Added ✓";
            button.disabled = true;
            button.style.background = "#28a745";
        }
    })
    .catch(error => console.error("Cart Error:", error));
}


// ================= LIVE SEARCH =================

document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");

    if (!searchInput || !searchResults) return;

    let timeout = null;

    searchInput.addEventListener("keyup", function () {

        clearTimeout(timeout);

        const query = this.value.trim();

        if (query.length === 0) {
            searchResults.innerHTML = "";
            searchResults.style.display = "none";
            return;
        }

        // small delay to prevent too many requests
        timeout = setTimeout(() => {

            fetch(`/search?q=${query}`)
                .then(res => res.json())
                .then(data => {

                    searchResults.innerHTML = "";

                    if (!data || data.length === 0) {
                        searchResults.style.display = "none";
                        return;
                    }

                    data.forEach(product => {

                        const item = document.createElement("a");
                        item.href = `/product/${product.id}`;
                        item.className = "search-item";

                        item.innerHTML = `
                            <div>
                                <strong>${product.name}</strong><br>
                                ₹${product.price}
                            </div>
                        `;

                        searchResults.appendChild(item);
                    });

                    searchResults.style.display = "block";
                })
                .catch(error => {
                    console.error("Search Error:", error);
                });

        }, 300); // debounce delay

    });

    document.addEventListener("click", function(e) {
        if (!searchInput.contains(e.target) &&
            !searchResults.contains(e.target)) {
            searchResults.style.display = "none";
        }
    });

});


// ================= CLOSE MODAL OUTSIDE =================

window.onclick = function(event) {

    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    if (loginModal && event.target === loginModal) {
        closeLogin();
    }

    if (registerModal && event.target === registerModal) {
        closeRegister();
    }
};
