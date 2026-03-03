/* ================= CART FUNCTIONS ================= */

export function addToCart(productId) {

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


export function changeQty(productId, action) {

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

        if (data.removed) {

            if (row) row.remove();

            if (container && !row) {
                container.innerHTML = `
                    <button onclick="addToCart(${productId})">
                        Add to Cart
                    </button>
                `;
            }

            const totalEl = document.getElementById("cart-total");
            if (totalEl && data.total !== undefined) {
                totalEl.innerText = data.total;
            }

            return;
        }

        const qtyEl = document.getElementById(`qty-${productId}`);
        if (qtyEl && data.quantity !== undefined) {
            qtyEl.innerText = data.quantity;
        }

        const subtotalEl = document.getElementById(`subtotal-${productId}`);
        if (subtotalEl && data.subtotal !== undefined) {
            subtotalEl.innerText = data.subtotal;
        }

        const totalEl = document.getElementById("cart-total");
        if (totalEl && data.total !== undefined) {
            totalEl.innerText = data.total;
        }

    })
    .catch(err => console.error("Quantity Update Error:", err));
}
