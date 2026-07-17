from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "campuslostandfound"
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@0977",
    database="lost_found_db"
)

cursor = db.cursor()

# Home Page
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        sql = "SELECT * FROM users WHERE email=%s AND password=%s"
        values = (email, password)

        cursor.execute(sql, values)

        user = cursor.fetchone()

        if user:
            return render_template("dashboard.html")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        register_number = request.form["register_number"]
        email = request.form["email"]
        password = request.form["password"]

        sql = """
        INSERT INTO users(full_name, register_number, email, password)
        VALUES(%s, %s, %s, %s)
        """

        values = (full_name, register_number, email, password)

        cursor.execute(sql, values)
        db.commit()

        return "Registration Successful!"

    return render_template("register.html")


@app.route('/lost_item', methods=['GET', 'POST'])
def lost_item():

    if request.method == "POST":

        item_name = request.form["item_name"]
        category = request.form["category"]
        location = request.form["location"]
        date_lost = request.form["date"]
        description = request.form["description"]

        sql = """
        INSERT INTO lost_items
        (item_name, category, location, date_lost, description)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (item_name, category, location, date_lost, description)

        cursor.execute(sql, values)
        db.commit()

        flash("✅ Lost Item Reported Successfully!")
        return redirect(url_for("home"))

    return render_template("lost_item.html")
@app.route('/view_lost_items')
def view_lost_items():

    sql = "SELECT * FROM lost_items"
    cursor.execute(sql)

    items = cursor.fetchall()

    return render_template("view_lost_items.html", items=items)


@app.route('/search_items', methods=['GET', 'POST'])
def search_items():

    items = []

    if request.method == "POST":

        search = request.form["search"]

        sql = "SELECT * FROM lost_items WHERE item_name LIKE %s"

        cursor.execute(sql, ('%' + search + '%',))

        items = cursor.fetchall()

    return render_template("search_items.html", items=items)


@app.route('/found_item', methods=['GET', 'POST'])
def found_item():

    if request.method == "POST":

        item_name = request.form["item_name"]
        category = request.form["category"]
        location = request.form["location"]
        date_found = request.form["date"]
        description = request.form["description"]

        sql = """
        INSERT INTO found_items
        (item_name, category, location, date_found, description)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (item_name, category, location, date_found, description)

        cursor.execute(sql, values)
        db.commit()

        return "Found Item Reported Successfully!"

    return render_template("found_item.html")


@app.route('/view_found_items')
def view_found_items():

    sql = "SELECT * FROM found_items"
    cursor.execute(sql)

    items = cursor.fetchall()

    return render_template("view_found_items.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)