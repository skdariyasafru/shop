from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "secret123"

# If running locally (not Render)
DB_NAME = "your_db_name"
DB_USER = "user1"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Render provides DATABASE_URL automatically
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    if DATABASE_URL:
        # Render PostgreSQL connection
        return psycopg2.connect(DATABASE_URL)
    else:
        # Local PostgreSQL connection
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

@app.route("/")
def home():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    db.close()
    return render_template("index.html", products=products)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )
        db.commit()
        cur.close()
        db.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cur.fetchone()
        cur.close()
        db.close()

        if user:
            session["user"] = user[1]
            return redirect("/")

    return render_template("login.html")

@app.route("/add/<int:id>")
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(id)
    return redirect("/cart")

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])

    if not cart_items:
        return render_template("cart.html", products=[])

    db = get_db()
    cur = db.cursor()

    # Fix for single item tuple
    cur.execute("SELECT * FROM products WHERE id = ANY(%s)", (cart_items,))
    products = cur.fetchall()

    cur.close()
    db.close()

    return render_template("cart.html", products=products)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO products(name,price) VALUES(%s,%s)",
            (name, price)
        )
        db.commit()
        cur.close()
        db.close()

    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
