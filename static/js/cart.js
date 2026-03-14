/* ================= CART FUNCTIONS ================= */

window.addToCart = function(productId) {

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

        if (!data) return;

        const container = document.getElementById(`cart-control-${productId}`);
        if (!container) return;

        const qty = data.quantity || 1;

        /* Check if quantity element already exists */
        const qtyEl = document.getElementById(`qty-${productId}`);

        if (qtyEl) {
            /* Just update number */
            qtyEl.innerText = qty;
        } 
        else {
            /* Replace Add to Cart button with qty controls */
            container.innerHTML = `
                <div class="qty-control">
                    <button class="qty-btn"
                        onclick="changeQty(${productId}, 'decrease')">-</button>

                    <span id="qty-${productId}" class="qty-number">
                        ${qty}
                    </span>

                    <button class="qty-btn"
                        onclick="changeQty(${productId}, 'increase')">+</button>
                </div>
            `;
        }

        updateCartCount(data.cart_count);

    })
    .catch(err => console.error("Add To Cart Error:", err));
};


/* ================= CHANGE QUANTITY ================= */

window.changeQty = function(productId, action) {

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

        /* Product removed */
        if (data.removed) {

            if (row) row.remove();

            if (container && !row) {
                container.innerHTML = `
                    <button onclick="addToCart(${productId})">
                        Add to Cart
                    </button>
                `;
            }

            updateCartCount(data.cart_count);

            const totalEl = document.getElementById("cart-total");
            if (totalEl && data.total !== undefined) {
                totalEl.innerText = data.total;
            }

            return;
        }

        /* Update quantity */
        const qtyEl = document.getElementById(`qty-${productId}`);
        if (qtyEl) {
            qtyEl.innerText = data.quantity;
        }

        /* Update subtotal on cart page */
        const subtotalEl = document.getElementById(`subtotal-${productId}`);
        if (subtotalEl) {
            subtotalEl.innerText = data.subtotal;
        }

        /* Update cart total */
        const totalEl = document.getElementById("cart-total");
        if (totalEl) {
            totalEl.innerText = data.total;
        }

        updateCartCount(data.cart_count);

    })
    .catch(err => console.error("Quantity Update Error:", err));
};


/* ================= CART COUNT ================= */

function updateCartCount(count) {

    const el = document.getElementById("cartCount");
    if (!el) return;

    el.innerText = count;
}
