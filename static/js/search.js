document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("indexSearch");
    const container = document.getElementById("productContainer");

    if (!searchInput) return;

    let debounce;

    searchInput.addEventListener("input", function () {

        clearTimeout(debounce);

        const query = this.value.trim();

        debounce = setTimeout(() => {

            /* ===== IF SEARCH EMPTY → RELOAD PAGE ===== */
            if (query.length === 0) {
                window.location.href = "/";
                return;
            }

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
                .catch(err => {
                    console.error("Search error:", err);
                });

        }, 300);

    });

});
