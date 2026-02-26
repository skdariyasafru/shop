// ================= ADD TO CART =================

function addToCart(id, btn = null) {

    fetch("/add_to_cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => {

        // If not logged in
        if (response.status === 401) {
            window.location.href = "/?login=1";
            return;
        }

        return response.json();
    })
    .then(data => {

        if (!data) return;

        if (data.status === "added") {

            // If button passed, change its state
            if (btn) {
                btn.innerText = "Added ✓";
                btn.style.backgroundColor = "#28a745";
                btn.disabled = true;
            }

            console.log("Item added to cart");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}



// ================= UPDATE CART =================

function updateCart(productId, action) {

    fetch("/update_cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
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

        // Update quantity
        const qtyElement = document.getElementById(`qty-${productId}`);
        if (qtyElement) {
            qtyElement.innerText = data.quantity;
        }

        // Update subtotal
        const subtotalElement = document.getElementById(`subtotal-${productId}`);
        if (subtotalElement) {
            subtotalElement.innerText = "₹" + data.subtotal;
        }

        // Update total
        const totalElement = document.getElementById("cart-total");
        if (totalElement) {
            totalElement.innerText = "₹" + data.total;
        }

    })
    .catch(error => console.error("Error:", error));
}
