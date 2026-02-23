/* =====================================================
   INDEX MART - MAIN JS (Clean + Stable Version)
===================================================== */


/* ================= LOGIN / REGISTER MODALS ================= */

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


/* ================= ADD TO CART ================= */

function addToCart(productId, button) {

    if (!productId) return;

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
            return null;
        }

        return response.json();
    })
    .then(data => {

        if (data && data.status === "added" && button) {

            // Visual feedback
            button.innerHTML = "Added ✓";
            button.disabled = true;

            button.style.backgroundColor = "#28a745";
            button.style.color = "#fff";
            button.style.cursor = "not-allowed";
            button.style.opacity = "0.9";
        }

    })
    .catch(error => {
        console.error("Add to Cart Error:", error);
    });
}


/* ================= LIVE SEARCH ================= */

document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");

    if (!searchInput || !searchResults) return;

    let debounceTimer;

    searchInput.addEventListener("input", function () {

        clearTimeout(debounceTimer);

        const query = this.value.trim();

        if (query.length < 2) {
            searchResults.innerHTML = "";
            searchResults.style.display = "none";
            return;
        }

        debounceTimer = setTimeout(() => {

            fetch(`/search?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
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

    // Hide search dropdown when clicking outside
    document.addEventListener("click", function (e) {
        if (!searchInput.contains(e.target) &&
            !searchResults.contains(e.target)) {
            searchResults.style.display = "none";
        }
    });

});


/* ================= CLOSE MODAL ON OUTSIDE CLICK ================= */

window.addEventListener("click", function (event) {

    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    if (loginModal && event.target === loginModal) {
        closeLogin();
    }

    if (registerModal && event.target === registerModal) {
        closeRegister();
    }
});
