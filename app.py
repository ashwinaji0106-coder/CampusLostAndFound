from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import mysql.connector
import os

app = Flask(__name__)
load_dotenv()
app.secret_key = "campuslostandfound"

# -----------------------------
# Upload Folder
# -----------------------------
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Database Connection
# -----------------------------
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    ssl_ca="ca.pem"
)
cursor = db.cursor(buffered=True)

# -----------------------------
# Home
# -----------------------------
@app.route('/')
def home():
    return render_template("index.html")

# -----------------------------
# Dashboard
# -----------------------------
@app.route('/dashboard')
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        full_name=session["full_name"]
    )

# -----------------------------
# Login
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        sql = """
        SELECT *
        FROM users
        WHERE email=%s AND password=%s
        """

        cursor.execute(sql, (email, password))

        user = cursor.fetchone()

        if user:

            session["user_id"] = user[0]
            session["full_name"] = user[1]

            flash("Login Successful!")

            return redirect(url_for("dashboard"))

        else:

            flash("Invalid Email or Password!")

            return redirect(url_for("login"))

    return render_template("login.html")

# -----------------------------
# Register
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        register_number = request.form["register_number"]
        department = request.form["department"]
        email = request.form["email"]
        password = request.form["password"]

        sql = """
        INSERT INTO users
        (full_name, register_number, department, email, password)
        VALUES (%s,%s,%s,%s,%s)
        """

        cursor.execute(sql, (
            full_name,
            register_number,
            department,
            email,
            password
        ))

        db.commit()

        flash("Registration Successful!")

        return redirect(url_for("login"))

    return render_template("register.html")
    # -----------------------------
# Report Lost Item
# -----------------------------
@app.route('/lost_item', methods=['GET', 'POST'])
def lost_item():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        item_name = request.form["item_name"]
        category = request.form["category"]
        location = request.form["location"]
        date_lost = request.form["date"]
        description = request.form["description"]

        image = request.files["image"]

        filename = ""

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        sql = """
        INSERT INTO lost_items
        (item_name, category, location, date_lost, description, image)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            item_name,
            category,
            location,
            date_lost,
            description,
            filename
        )

        cursor.execute(sql, values)
        db.commit()

        flash("Lost Item Reported Successfully!")

        return redirect(url_for("dashboard"))

    return render_template("lost_item.html")


# -----------------------------
# View Lost Items
# -----------------------------
@app.route('/view_lost_items')
def view_lost_items():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor.execute("SELECT * FROM lost_items")

    items = cursor.fetchall()

    return render_template(
        "view_lost_items.html",
        items=items
    )


# -----------------------------
# Search Lost Items
# -----------------------------
@app.route('/search_items', methods=['GET', 'POST'])
def search_items():

    if "user_id" not in session:
        return redirect(url_for("login"))

    items = []

    if request.method == "POST":

        search = request.form["search"]

        sql = """
        SELECT *
        FROM lost_items
        WHERE item_name LIKE %s
        OR category LIKE %s
        OR location LIKE %s
        """

        cursor.execute(sql, (
            '%' + search + '%',
            '%' + search + '%',
            '%' + search + '%'
        ))

        items = cursor.fetchall()

    return render_template(
        "search_items.html",
        items=items
    )
    # -----------------------------
# Report Found Item
# -----------------------------
@app.route('/found_item', methods=['GET', 'POST'])
def found_item():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        item_name = request.form["item_name"]
        category = request.form["category"]
        location = request.form["location"]
        date_found = request.form["date"]
        description = request.form["description"]

        image = request.files["image"]

        filename = ""

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        sql = """
        INSERT INTO found_items
        (item_name, category, location, date_found, description, image)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            item_name,
            category,
            location,
            date_found,
            description,
            filename
        )

        cursor.execute(sql, values)
        db.commit()

        flash("Found Item Reported Successfully!")

        return redirect(url_for("dashboard"))

    return render_template("found_item.html")


# -----------------------------
# View Found Items
# -----------------------------
@app.route('/view_found_items')
def view_found_items():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor.execute("SELECT * FROM found_items")

    items = cursor.fetchall()

    return render_template(
        "view_found_items.html",
        items=items
    )


# -----------------------------
# Logout
# -----------------------------
@app.route('/logout')
def logout():

    session.clear()

    flash("Logged Out Successfully!")

    return redirect(url_for("home"))
    # -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)