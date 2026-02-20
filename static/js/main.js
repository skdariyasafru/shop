function openLogin() {
    document.getElementById("loginModal").style.display = "block";
}

function closeLogin() {
    document.getElementById("loginModal").style.display = "none";
}

function openRegister() {
    document.getElementById("registerModal").style.display = "block";
}

function closeRegister() {
    document.getElementById("registerModal").style.display = "none";
}

function switchToRegister() {
    closeLogin();
    openRegister();
}

function switchToLogin() {
    closeRegister();
    openLogin();
}
// add item
function addToCart(productId, button) {

    fetch("/add_to_cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id: productId })
    })
    .then(response => {
        if (response.status === 401) {
            openLogin();
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.status === "added") {

            // 🔥 Change button text
            button.innerText = "Added ✓";

            // 🔥 Disable button
            button.disabled = true;

            // 🔥 Change button color
            button.style.background = "#28a745";
            button.style.cursor = "not-allowed";
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        let query = this.value.trim();

        if (query.length < 1) {
            searchResults.style.display = "none";
            return;
        }

        fetch(`/search?q=${query}`)
            .then(res => res.json())
            .then(data => {

                searchResults.innerHTML = "";

                if (data.length === 0) {
                    searchResults.style.display = "none";
                    return;
                }

                data.forEach(product => {

                    searchResults.innerHTML += `
                        <div class="search-item"
                             onclick="window.location='/product/${product.id}'">

                            <img src="${product.image}" alt="${product.name}">
                            <div>
                                <h4>${product.name}</h4>
                                <p>₹${product.price}</p>
                            </div>
                        </div>
                    `;
                });

                searchResults.style.display = "block";
            });
    });

    // Hide dropdown when clicking outside
    document.addEventListener("click", function(e) {
        if (!searchInput.contains(e.target) &&
            !searchResults.contains(e.target)) {
            searchResults.style.display = "none";
        }
    });
}


//end item


window.onclick = function(event) {
    if (event.target == document.getElementById("loginModal")) {
        closeLogin();
    }
    if (event.target == document.getElementById("registerModal")) {
        closeRegister();
    }
};
