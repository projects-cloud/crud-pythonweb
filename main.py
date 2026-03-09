from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("index.html", products=products)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price) VALUES (?, ?)",
            (name, price)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("create.html")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        cursor.execute(
            "UPDATE products SET name = ?, price = ? WHERE id = ?",
            (name, price, id)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
    product = cursor.fetchone()
    conn.close()
    return render_template("edit.html", product=product)

if __name__ == "__main__":
    app.run(debug=True)