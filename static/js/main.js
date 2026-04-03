/* =====================================================
   INDEX MART - MAIN.JS (CLEAN)
===================================================== */


/* ================= AUTO LOGIN CHECK ================= */

document.addEventListener("DOMContentLoaded", function () {

    const params = new URLSearchParams(window.location.search);

    if (params.get("login") === "1") return;

    fetch("/check_login")
    .then(res => res.json())
    .then(data => {

        if (window.location.pathname === "/" && !data.logged_in) {
            if (typeof openLogin === "function") {
                openLogin();
            }
        }

    })
    .catch(err => console.error("Login check error:", err));

});


/* ================= ADD TO CART ================= */

function addToCart(productId) {

    fetch("/add_to_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: productId })
    })
    .then(res => {

        if (res.status === 401) {
            if (typeof openLogin === "function") {
                openLogin();
            }
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
                <button onclick="changeQty(${productId}, 'decrease')">-</button>
                <span id="qty-${productId}">${data.quantity}</span>
                <button onclick="changeQty(${productId}, 'increase')">+</button>
            </div>
        `;
    })
    .catch(err => console.error("Add To Cart Error:", err));
}


/* ================= CHANGE QTY ================= */

function changeQty(productId, action) {

    fetch("/update_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: productId, action: action })
    })
    .then(res => {

        if (res.status === 401) {
            if (typeof openLogin === "function") {
                openLogin();
            }
            return null;
        }

        return res.json();
    })
    .then(data => {

        if (!data) return;

        const qtyEl = document.getElementById(`qty-${productId}`);
        if (qtyEl) qtyEl.innerText = data.quantity;

    })
    .catch(err => console.error("Qty Error:", err));
}


/* ================= SEARCH ================= */

document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("indexSearch");
    const container = document.getElementById("productContainer");

    if (!searchInput || !container) return;

    let debounce;

    searchInput.addEventListener("input", function () {

        clearTimeout(debounce);

        const query = this.value.trim();

        debounce = setTimeout(() => {

            fetch("/search?q=" + encodeURIComponent(query))
            .then(res => res.json())
            .then(products => {

                container.innerHTML = "";

                if (!products || products.length === 0) {
                    container.innerHTML = "<p>No products found</p>";
                    return;
                }

                products.forEach(p => {

                    const card = document.createElement("div");

                    card.innerHTML = `
                        <img src="${p.image}">
                        <h3>${p.name}</h3>
                        <p>₹${p.price}</p>
                        <button onclick="addToCart(${p.id})">Add to Cart</button>
                    `;

                    container.appendChild(card);

                });

            })
            .catch(err => console.error("Search error:", err));

        }, 300);

    });

});
