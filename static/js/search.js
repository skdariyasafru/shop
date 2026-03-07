document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("indexSearch");
    const container = document.getElementById("productContainer");

    if (!searchInput || !container) return;

    let debounce;
    let lastQuery = "";

    searchInput.addEventListener("input", function () {

        const query = this.value.trim();

        // avoid duplicate calls
        if (query === lastQuery) return;

        lastQuery = query;

        clearTimeout(debounce);

        debounce = setTimeout(() => {

            // loading message
            container.innerHTML = "<p>Searching...</p>";

            fetch("/search?q=" + encodeURIComponent(query))
                .then(res => res.json())
                .then(products => {

                    container.innerHTML = "";

                    if (!products || products.length === 0) {

                        if (query === "") {
                            container.innerHTML = "<p>No products available</p>";
                        } else {
                            container.innerHTML = "<p>No products found</p>";
                        }

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
                .catch(error => {

                    console.error("Search error:", error);

                    container.innerHTML = "<p>Search failed. Try again.</p>";

                });

        }, 300); // debounce time

    });

});
