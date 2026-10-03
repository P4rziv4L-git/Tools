import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(BASE_DIR, "database", "tool_library.db")

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT,
    join_date TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tools (
    tool_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER,
    brand TEXT,
    serial_no TEXT UNIQUE,
    purchase_date TEXT,
    purchase_price REAL,
    status TEXT NOT NULL DEFAULT 'Available',

    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    tool_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    condition_out TEXT,
    condition_in TEXT,
    late_fee REAL DEFAULT 0,

    FOREIGN KEY (member_id)
        REFERENCES members(member_id),

    FOREIGN KEY (tool_id)
        REFERENCES tools(tool_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

connection.commit()

connection.close()

print("Database created successfully!")
