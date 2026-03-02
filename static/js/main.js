/* =====================================================
   INDEX MART - AUTO RELOAD VERSION
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


/* ================= AUTO OPEN LOGIN ================= */

document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    if (params.get("login") === "1") {
        openLogin();
    }
});


/* =====================================================
   ADD TO CART
===================================================== */

function addToCart(productId) {

    fetch("/add_to_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: productId })
    })
    .then(response => {

        if (response.status === 401 || response.status === 302) {
            window.location.href = "/?login=1";
            return null;
        }

        return response.json();
    })
    .then(data => {

        if (!data || data.status !== "added") return;

        const container = document.getElementById(`cart-control-${productId}`);
        if (!container) return;

        container.innerHTML = `
            <div class="qty-control">
                <button class="qty-btn"
                    onclick="changeQty(${productId}, 'decrease')">-</button>

                <span id="qty-${productId}" class="qty-number">
                    ${data.quantity}
                </span>

                <button class="qty-btn"
                    onclick="changeQty(${productId}, 'increase')">+</button>
            </div>
        `;
    })
    .catch(error => console.error("Add To Cart Error:", error));
}


/* =====================================================
   CHANGE QUANTITY (+ / -)
===================================================== */

function changeQty(productId, action) {

    fetch("/update_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: productId,
            action: action
        })
    })
    .then(response => {

        if (response.status === 401 || response.status === 302) {
            window.location.href = "/?login=1";
            return null;
        }

        return response.json();
    })
    .then(data => {

        if (!data) return;

        const currentPath = window.location.pathname;

        /* ===== IF ON CART PAGE → AUTO RELOAD ===== */
        if (currentPath === "/cart") {

            // small delay for smooth UX
            setTimeout(() => {
                location.reload();
            }, 200);

            return;
        }

        /* ===== INDEX PAGE LIVE UPDATE ===== */

        if (data.removed) {
            const container = document.getElementById(`cart-control-${productId}`);
            if (container) {
                container.innerHTML = `
                    <button onclick="addToCart(${productId})">
                        Add to Cart
                    </button>
                `;
            }
            return;
        }

        const qtyEl = document.getElementById(`qty-${productId}`);
        if (qtyEl && data.quantity !== undefined) {
            qtyEl.innerText = data.quantity;
        }

    })
    .catch(error => console.error("Quantity Update Error:", error));
}


/* =====================================================
   LIVE SEARCH
===================================================== */

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
                });

        }, 300);
    });

});
