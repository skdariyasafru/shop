from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "secret123"

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
            CREATE TABLE users1 (
                 id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                  email VARCHAR(100),
                     password VARCHAR(100),
                     type varchar(100)
                )
        """)

    
    conn.commit()
    cur.close()    
    conn.close()
     cur.execute("""
            CREATE TABLE products 
                (
                  id SERIAL PRIMARY KEY,
                  name VARCHAR(100),
                  price NUMERIC
                )
                """)

    
    conn.commit()
    cur.close()    
    conn.close()


    
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    return render_template("index.html", products=products)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
                    (name,email,password))
        db.commit()
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s",
                    (email,password))
        user = cur.fetchone()

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
    cur.execute("SELECT * FROM products WHERE id IN %s", (tuple(cart_items),))
    products = cur.fetchall()

    return render_template("cart.html", products=products)

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO products(name,price) VALUES(%s,%s)", (name,price))
        db.commit()

    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
