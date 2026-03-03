/* =====================================================
   INDEX MART - COMPLETE MAIN.JS (MERGED VERSION)
===================================================== */


/* =====================================================
   AUTH / MODAL FUNCTIONS
===================================================== */

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


/* =====================================================
   AUTO OPEN LOGIN (?login=1)
===================================================== */

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
    .then(res => {

        if (res.status === 401) {
            window.location.href = "/?login=1";
            return null;
        }

        return res.json();
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
    .catch(err => console.error("Add To Cart Error:", err));
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
    .then(res => {

        if (res.status === 401) {
            window.location.href = "/?login=1";
            return null;
        }

        return res.json();
    })
    .then(data => {

        if (!data) return;

        const row = document.getElementById(`row-${productId}`);
        const container = document.getElementById(`cart-control-${productId}`);

        /* ===== ITEM REMOVED ===== */
        if (data.removed) {

            // Cart page → remove row
            if (row) row.remove();

            // Index page → revert to Add button
            if (container && !row) {
                container.innerHTML = `
                    <button onclick="addToCart(${productId})">
                        Add to Cart
                    </button>
                `;
            }

            // Update total
            const totalEl = document.getElementById("cart-total");
            if (totalEl && data.total !== undefined) {
                totalEl.innerText = data.total;
            }

            return;
        }

        /* ===== UPDATE QUANTITY ===== */
        const qtyEl = document.getElementById(`qty-${productId}`);
        if (qtyEl && data.quantity !== undefined) {
            qtyEl.innerText = data.quantity;
        }

        /* ===== UPDATE SUBTOTAL ===== */
        const subtotalEl = document.getElementById(`subtotal-${productId}`);
        if (subtotalEl && data.subtotal !== undefined) {
            subtotalEl.innerText = data.subtotal;
        }

        /* ===== UPDATE TOTAL ===== */
        const totalEl = document.getElementById("cart-total");
        if (totalEl && data.total !== undefined) {
            totalEl.innerText = data.total;
        }

    })
    .catch(err => console.error("Quantity Update Error:", err));
}


/* =====================================================
   CLOSE MODAL OUTSIDE CLICK
===================================================== */

window.addEventListener("click", function (event) {

    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    if (loginModal && event.target === loginModal) closeLogin();
    if (registerModal && event.target === registerModal) closeRegister();
});


console.log("Index Mart Main JS Loaded Successfully");
