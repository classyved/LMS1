from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

# Dummy in-memory database for demonstration purposes
books = []
issued_books = []

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # Add database logic here
    if username == "admin" and password == "admin123":
        return redirect(url_for("admin_dashboard"))
    elif username == "user" and password == "user123":
        return redirect(url_for("user_dashboard"))
    else:
        flash("Invalid credentials")
        return redirect(url_for("home"))

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/user_dashboard")
def user_dashboard():
    return render_template("user_dashboard.html")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        available = int(request.form["available"])
        books.append({"title": title, "author": author, "category": category, "available": available})
        flash("Book added successfully!")
        return redirect(url_for("admin_dashboard"))
    return render_template("add_book.html")

@app.route("/update_book", methods=["GET", "POST"])
def update_book():
    if request.method == "POST":
        title = request.form["title"]
        new_copies = int(request.form["new_copies"])
        for book in books:
            if book["title"] == title:
                book["available"] = new_copies
                flash("Book updated successfully!")
                return redirect(url_for("admin_dashboard"))
        flash("Book not found!")
    return render_template("update_book.html")

@app.route("/issue_book", methods=["GET", "POST"])
def issue_book():
    if request.method == "POST":
        user_id = request.form["user_id"]
        book_id = request.form["book_id"]
        issue_date = request.form["issue_date"]
        for book in books:
            if book["title"] == book_id and book["available"] > 0:
                book["available"] -= 1
                issued_books.append({"user_id": user_id, "book_id": book_id, "issue_date": issue_date})
                flash("Book issued successfully!")
                return redirect(url_for("admin_dashboard"))
        flash("Book not available!")
    return render_template("issue_book.html")

@app.route("/return_book", methods=["GET", "POST"])
def return_book():
    if request.method == "POST":
        user_id = request.form["user_id"]
        book_id = request.form["book_id"]
        return_date = request.form["return_date"]
        for issue in issued_books:
            if issue["user_id"] == user_id and issue["book_id"] == book_id:
                issued_books.remove(issue)
                for book in books:
                    if book["title"] == book_id:
                        book["available"] += 1
                        flash("Book returned successfully!")
                        return redirect(url_for("admin_dashboard"))
        flash("Issued book record not found!")
    return render_template("return_book.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/reports/active_issues")
def active_issues():
    return render_template("active_issues.html", issued_books=issued_books)

@app.route("/reports/overdue_returns")
def overdue_returns():
    # For now, simulate overdue logic
    overdue_books = [issue for issue in issued_books if issue["user_id"] == "overdue_user"]
    return render_template("overdue_returns.html", overdue_books=overdue_books)

@app.route("/reports/master_list_books")
def master_list_books():
    return render_template("master_list_books.html", books=books)

@app.route("/reports/master_list_members")
def master_list_members():
    # Simulate membership data
    members = [{"user_id": "1", "name": "John Doe"}, {"user_id": "2", "name": "Jane Smith"}]
    return render_template("master_list_members.html", members=members)
# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

@app.route("/reports/master_list_books", endpoint="master_list_books_route")
def master_list_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template("master_list_books.html", books=books)

@app.route("/reports/master_list_members", endpoint="master_list_members_route")
def master_list_members():
    conn = get_db_connection()
    members = conn.execute('SELECT * FROM members').fetchall()
    conn.close()
    return render_template("master_list_members.html", members=members)
if __name__ == "__main__":
    app.run(debug=True)
