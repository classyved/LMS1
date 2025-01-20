import sqlite3

def setup_database():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Create books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)

    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            issue_date DATE NOT NULL,
            return_date DATE,
            fine REAL DEFAULT 0.0,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Insert default users
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "admin123", "admin"))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("user", "user123", "user"))
    except sqlite3.IntegrityError:
        pass  # Skip if already inserted

    connection.commit()
    connection.close()

def add_book(title, author, category):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (title, author, category) VALUES (?, ?, ?)", (title, author, category))
    connection.commit()
    connection.close()

def remove_book(book_id):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()
    connection.close()

def add_user(username, password, role):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    except sqlite3.IntegrityError:
        print("User already exists.")
    connection.commit()
    connection.close()

def remove_user(user_id):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    connection.commit()
    connection.close()

if __name__ == "__main__":
    setup_database()
