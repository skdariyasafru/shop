// ===============================
// Grocery Store Frontend Script
// ===============================

// Load products when page opens
document.addEventListener("DOMContentLoaded", loadProducts);

// Store products globally for search
let allProducts = [];


// ===============================
// Load Products from Backend
// ===============================

function loadProducts() {

  fetch("/products")
    .then(res => res.json())
    .then(data => {
      allProducts = data;
      displayProducts(data);
    })
    .catch(err => {
      console.error("Error loading products:", err);
    });

}


// ===============================
// Display Products
// ===============================

function displayProducts(products) {

  const container = document.getElementById("products");

  if (!container) return;

  container.innerHTML = "";

  if (products.length === 0) {
    container.innerHTML = "<p>No products available</p>";
    return;
  }

  products.forEach(p => {

    container.innerHTML += `
      <div class="card">
        <img src="${p.image}" alt="${p.name}" width="120">
        <h3>${p.name}</h3>
        <p>₹${p.price}</p>

        <button onclick='addToCart("${p.name}", ${p.price})'>
          Add to Cart
        </button>
      </div>
    `;

  });

}


// ===============================
// Search Products
// ===============================

function searchProducts() {

  const text = document
    .getElementById("search")
    .value
    .toLowerCase();

  const filtered = allProducts.filter(p =>
    p.name.toLowerCase().includes(text)
  );

  displayProducts(filtered);

}


// ===============================
// Add to Cart
// ===============================

function addToCart(name, price) {

  fetch("/add_to_cart", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      name: name,
      price: price
    })
  })
  .then(res => res.json())
  .then(() => {
    alert("✅ Added to cart!");
  })
  .catch(err => {
    console.error("Cart error:", err);
    alert("Login required!");
  });

}


// ===============================
// Admin: Add Product
// ===============================

function addProduct() {

  const name = document.getElementById("name").value;
  const price = parseFloat(document.getElementById("price").value);
  const image = document.getElementById("image"
