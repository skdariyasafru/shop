/* =====================================================
INDEX MART - COMPLETE MAIN.JS
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

```
const params = new URLSearchParams(window.location.search);

if (params.get("login") === "1") {
    openLogin();
}
```

});

/* =====================================================
AUTO LOGIN CHECK (NEW FEATURE - SAFE)
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

```
const params = new URLSearchParams(window.location.search);

// Do not override existing ?login=1 logic
if (params.get("login") === "1") return;

fetch("/check_login")
.then(res => res.json())
.then(data => {

    // only trigger on homepage
    if (window.location.pathname === "/" && !data.logged_in) {
        openLogin();
    }

})
.catch(err => console.error("Login check error:", err));
```

});

/* =====================================================
ADD TO CART
===================================================== */

function addToCart(productId) {

```
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
```

}

/* =====================================================
CHANGE QUANTITY (+ / -)
===================================================== */

function changeQty(productId, action) {

```
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
```

}

/* =====================================================
LIVE SEARCH
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

```
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
                card.className = "card";

                const imageHTML = p.image
                    ? `<img src="${p.image}" alt="${p.name}">`
                    : `<div class="image-placeholder"></div>`;

                card.innerHTML = `
                    ${imageHTML}
                    <h3>${p.name}</h3>
                    <p class="price">₹${p.price}</p>

                    <div id="cart-control-${p.id}">
                        <button onclick="addToCart(${p.id})">
                            Add to Cart
                        </button>
                    </div>
                `;

                container.appendChild(card);

            });

        })
        .catch(err => console.error("Search error:", err));

    }, 300);

});
```

});

/* =====================================================
CLOSE MODAL OUTSIDE CLICK
===================================================== */

window.addEventListener("click", function (event) {

```
const loginModal = document.getElementById("loginModal");
const registerModal = document.getElementById("registerModal");

if (loginModal && event.target === loginModal) closeLogin();
if (registerModal && event.target === registerModal) closeRegister();
```

});

console.log("Index Mart Main JS Loaded Successfully");
