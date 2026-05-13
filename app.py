from flask import Flask, render_template, request, redirect, url_for, session
from chatbot_logic import get_response
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecretkey"
app.permanent_session_lifetime = 0
app.config["SESSION_PERMANENT"] = False

# Home page (Protected Chatbot)
@app.route("/")
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html", username=session["user"])


# Chatbot response
@app.route("/get", methods=["POST"])
def chatbot():

    user_msg = request.form["message"]

    return get_response(user_msg)

# Register page
# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (
                first_name, last_name, email, phone, username, password
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            first_name, last_name, email, phone, username, password
        ))

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":

           session.clear()
        session["user"] = username

        return redirect(url_for("home"))

        return "Invalid username or password"

    return render_template("login.html")


# Admin page
@app.route("/admin")
def admin():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("admin.html")


# Add chatbot data
@app.route("/add", methods=["POST"])
def add_data():

    if "user" not in session:
        return redirect(url_for("login"))

    keyword = request.form["keyword"]
    response = request.form["response"]

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO responses (keyword, response) VALUES (?, ?)",
        (keyword, response)
    )

    conn.commit()
    conn.close()

    return "Data added successfully!"


# View all chatbot data
@app.route("/view")
def view_data():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM responses")
    data = cursor.fetchall()

    conn.close()

    return render_template("view.html", data=data)


# Delete chatbot data
@app.route("/delete/<int:id>")
def delete_data(id):

    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM responses WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("view_data"))


# Edit chatbot data
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_data(id):

    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    if request.method == "POST":

        keyword = request.form["keyword"]
        response = request.form["response"]

        cursor.execute(
            "UPDATE responses SET keyword=?, response=? WHERE id=?",
            (keyword, response, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("view_data"))

    cursor.execute("SELECT * FROM responses WHERE id=?", (id,))
    data = cursor.fetchone()

    conn.close()

    return render_template("edit.html", data=data)


# Logout
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)