from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

def create_database():

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()

# -----------------------------------
# Main Page
# -----------------------------------


@app.route("/")
def home():

    return render_template("navbar.html")

# -----------------------------------
# Home Page
# -----------------------------------

@app.route("/home")
def home_page():

    return render_template("home.html")

# -----------------------------------
# Employee Page
# -----------------------------------

@app.route("/employee")
def employee():

    return render_template("employee.html")

# -----------------------------------
# Add Employee Page
# -----------------------------------

@app.route("/addemployee")
def addemployee():

    return render_template("addemployee.html")

# -----------------------------------
# Search Page
# -----------------------------------

@app.route("/search")
def search():

    return render_template("search.html")


# -----------------------------------
# Register Page
# -----------------------------------

@app.route("/register", methods=["GET"])
def register_page():

    return render_template("register.html")

# -----------------------------------
# Register Path
# -----------------------------------

@app.route("/register", methods=["POST"])
def register():

    fullname = request.form["fullname"]
    username = request.form["username"]
    password = request.form["password"]

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (fullname, username, password)
            VALUES (?, ?, ?)
        """, (fullname, username, password))

        connection.commit()

    except sqlite3.IntegrityError:

        connection.close()

        return """
        <h2>Username already exists!</h2>
        <a href="/register">Try Again</a>
        """

    connection.close()

    return redirect("/login")

# -----------------------------------
# Login Page
# -----------------------------------

@app.route("/login", methods=["GET"])
def login_page():

    return render_template("login.html")

 
# -----------------------------------
# Login Path
# -----------------------------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    connection.close()

    if user:

        return """
        <h2>Login successful!</h2>
        <p>Welcome, """ + username + """!</p>
        <a href="/">Go to Home</a>
        """

    else:

        return """
        <h2>Login failed!</h2>
        <p>Username or password is incorrect.</p>
        <a href="/login">Try Again</a>
        """


if __name__ == "__main__":

    create_database()

    app. run(debug=True)