
/* =====================================================
   INDEX MART - CLEAN PROFESSIONAL VERSION
===================================================== */


/* ================= MODAL FUNCTIONS ================= */

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


/* ================= AUTO OPEN LOGIN (?login=1) ================= */

document.addEventListener("DOMContentLoaded", function () {

    const params = new URLSearchParams(window.location.search);
    if (params.get("login") === "1") {
        openLogin();
    }

});


/* ================= ADD TO CART ================= */

function addToCart(productId, button = null) {

    if (!productId) return;

    fetch("/add_to_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: productId })
    })
    .then(response => {

        // If not logged in (Flask redirect)
        if (response.status === 302 || response.status === 401) {
            window.location.href = "/?login=1";
            return null;
        }

        return response.json();
    })
    .then(data => {

        if (!data) return;

        if (data.status === "added") {

            if (button) {
                button.innerText = "Added ✓";
                button.disabled = true;
                button.style.background = "#28a745";
                button.style.color = "#fff";
                button.style.cursor = "not-allowed";
            }

            console.log("Item added successfully");
        }

    })
    .catch(error => console.error("Add To Cart Error:", error));
}


/* ================= UPDATE CART ================= */

function updateCart(productId, action) {

    fetch("/update_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: productId,
            action: action
        })
    })
    .then(response => response.json())
    .then(data => {

        if (data.removed) {
            location.reload();
            return;
        }

        const qtyEl = document.getElementById(`qty-${productId}`);
        const subtotalEl = document.getElementById(`subtotal-${productId}`);
        const totalEl = document.getElementById("cart-total");

        if (qtyEl) qtyEl.innerText = data.quantity;
        if (subtotalEl) subtotalEl.innerText = "₹" + data.subtotal;
        if (totalEl) totalEl.innerText = "₹" + data.total;

    })
    .catch(error => console.error("Cart Update Error:", error));
}
function changeQty(productId, action) {

    fetch("/update_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: productId,
            action: action
        })
    })
    .then(response => response.json())
    .then(data => {

        if (data.removed) {
            const container = document.getElementById(`cart-control-${productId}`);
            if (container) {
                container.innerHTML = `
                    <button onclick="addToCart(${productId}, this)">
                        Add to Cart
                    </button>
                `;
            }
            return;
        }

        const qtyEl = document.getElementById(`qty-${productId}`);
        if (qtyEl) qtyEl.innerText = data.quantity;

    })
    .catch(error => {
        console.error("Quantity Error:", error);
    });
}

/* ================= LIVE SEARCH (NAVBAR DROPDOWN) ================= */

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
                .catch(error => console.error("Search Error:", error));

        }, 300);
    });

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
