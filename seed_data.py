import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(BASE_DIR, "database", "tool_library.db")

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

categories = [
    ("Power Tools",),
    ("Garden Tools",),
    ("Hand Tools",)
]

cursor.executemany("""
INSERT OR IGNORE INTO categories (category_name)
VALUES (?)
""", categories)

members = [
    ("Sarah Johnson", "821234567", "sarah.j@email.com",
     "12 Oak St", "2026-01-10"),

    ("Michael Brown", "829876543", "michael.b@email.com",
     "24 Pine St", "2026-02-15"),

    ("Emma Wilson", "824567891", "emma.w@email.com",
     "8 Birch St", "2026-03-05")
]

cursor.execute("SELECT COUNT(*) FROM members")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO members
    (name, phone, email, address, join_date)
    VALUES (?, ?, ?, ?, ?)
    """, members)

tools = [
    ("Cordless Drill", 1, "Bosch", "BSC-88421",
     "2025-01-15", 149.99, "Available"),

    ("Circular Saw", 1, "Makita", "MKT-33210",
     "2025-02-10", 199.99, "Available"),

    ("Hedge Trimmer", 2, "Ryobi", "RYB-55102",
     "2025-03-20", 129.99, "Available")
]

cursor.execute("SELECT COUNT(*) FROM tools")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO tools
    (name, category_id, brand, serial_no,
     purchase_date, purchase_price, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, tools)

connection.commit()

print("\nMEMBERS:")
cursor.execute("SELECT * FROM members")

for member in cursor.fetchall():
    print(member)

print("\nTOOLS:")
cursor.execute("""
SELECT
    tools.tool_id,
    tools.name,
    categories.category_name,
    tools.brand,
    tools.status
FROM tools
JOIN categories
ON tools.category_id = categories.category_id
""")

for tool in cursor.fetchall():
    print(tool)

connection.close()

print("\nSample data added successfully!")
