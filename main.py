import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
from datetime import date, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "tool_library.db")

root = tk.Tk()
root.title("Community Tool Library")
root.geometry("600x550")
root.resizable(False, False)


def login():
    username = username_entry.get()
    password = password_entry.get()

    # Fixed credentials are used for the project demo.
    if username == "kim" and password == "admin123":
        show_dashboard()
    else:
        messagebox.showerror(
            "Login Failed",
            "Incorrect username or password."
        )


def show_tools():

    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(
        root,
        text="Tool Inventory",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    columns = ("ID", "Tool", "Category", "Brand", "Status")

    table = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=10
    )

    for column in columns:
        table.heading(column, text=column)

    table.column("ID", width=50)
    table.column("Tool", width=150)
    table.column("Category", width=120)
    table.column("Brand", width=100)
    table.column("Status", width=100)

    table.pack(pady=10)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

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

    tools = cursor.fetchall()

    connection.close()

    for tool in tools:
        table.insert("", tk.END, values=tool)

    add_tool_button = tk.Button(
        root,
        text="Add New Tool",
        width=20,
        command=add_tool
    )
    add_tool_button.pack(pady=5)

    back_button = tk.Button(
        root,
        text="Back to Dashboard",
        width=20,
        command=show_dashboard
    )
    back_button.pack(pady=20)


def add_tool():

    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(
        root,
        text="Add New Tool",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    tk.Label(root, text="Tool Name:").pack()
    name_entry = tk.Entry(root, width=35)
    name_entry.pack(pady=5)

    tk.Label(root, text="Category:").pack()
    category_entry = tk.Entry(root, width=35)
    category_entry.pack(pady=5)

    tk.Label(root, text="Brand:").pack()
    brand_entry = tk.Entry(root, width=35)
    brand_entry.pack(pady=5)

    tk.Label(root, text="Status:").pack()
    status_combo = ttk.Combobox(
        root,
        values=["Available", "Borrowed", "Maintenance"],
        width=32,
        state="readonly"
    )
    status_combo.set("Available")
    status_combo.pack(pady=5)

    def save_tool():
        name = name_entry.get().strip()
        category = category_entry.get().strip()
        brand = brand_entry.get().strip()
        status = status_combo.get()

        if not name or not category or not brand:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        connection = None

        try:
            connection = sqlite3.connect(DATABASE_PATH)
            cursor = connection.cursor()

            cursor.execute(
                "SELECT category_id FROM categories WHERE category_name = ?",
                (category,)
            )

            result = cursor.fetchone()

            if result is None:
                messagebox.showerror(
                    "Category Not Found",
                    f"The category '{category}' does not exist."
                )
                return

            category_id = result[0]

            cursor.execute("""
                INSERT INTO tools (name, category_id, brand, status)
                VALUES (?, ?, ?, ?)
            """, (name, category_id, brand, status))

            connection.commit()

            messagebox.showinfo(
                "Tool Added",
                f"{name} has been added successfully."
            )

            show_tools()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:
            if connection:
                connection.close()

    save_button = tk.Button(
        root,
        text="Save Tool",
        width=20,
        command=save_tool
    )
    save_button.pack(pady=10)

    back_button = tk.Button(
        root,
        text="Back to Tools",
        width=20,
        command=show_tools
    )
    back_button.pack(pady=5)


def add_member():

    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(
        root,
        text="Add New Member",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    tk.Label(root, text="Name:").pack()
    name_entry = tk.Entry(root, width=35)
    name_entry.pack(pady=4)

    tk.Label(root, text="Phone:").pack()
    phone_entry = tk.Entry(root, width=35)
    phone_entry.pack(pady=4)

    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root, width=35)
    email_entry.pack(pady=4)

    tk.Label(root, text="Address:").pack()
    address_entry = tk.Entry(root, width=35)
    address_entry.pack(pady=4)

    tk.Label(root, text="Join Date (YYYY-MM-DD):").pack()
    join_date_entry = tk.Entry(root, width=35)
    join_date_entry.pack(pady=4)

    join_date_entry.insert(0, date.today().isoformat())

    def save_member():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()
        join_date = join_date_entry.get().strip()

        if not name or not phone:
            messagebox.showerror(
                "Missing Information",
                "Name and phone number are required."
            )
            return

        try:
            connection = sqlite3.connect(DATABASE_PATH)
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO members
                (name, phone, email, address, join_date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                phone,
                email,
                address,
                join_date
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Member Added",
                f"{name} has been added successfully."
            )

            show_dashboard()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    save_button = tk.Button(
        root,
        text="Add Member",
        width=20,
        command=save_member
    )
    save_button.pack(pady=15)

    back_button = tk.Button(
        root,
        text="Back to Members",
        width=20,
        command=show_members
    )
    back_button.pack(pady=5)

    name_entry.bind(
        "<Return>",
        lambda event: phone_entry.focus_set()
    )

    phone_entry.bind(
        "<Return>",
        lambda event: email_entry.focus_set()
    )

    email_entry.bind(
        "<Return>",
        lambda event: address_entry.focus_set()
    )

    address_entry.bind(
        "<Return>",
        lambda event: join_date_entry.focus_set()
    )

    join_date_entry.bind(
        "<Return>",
        lambda event: save_member()
    )

    name_entry.focus_set()

def show_members():

    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(
        root,
        text="Members",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    columns = ("ID", "Name", "Phone", "Email", "Join Date")

    table = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=10
    )

    table.heading("ID", text="ID")
    table.heading("Name", text="Name")
    table.heading("Phone", text="Phone")
    table.heading("Email", text="Email")
    table.heading("Join Date", text="Join Date")

    table.column("ID", width=40)
    table.column("Name", width=130)
    table.column("Phone", width=100)
    table.column("Email", width=160)
    table.column("Join Date", width=90)

    table.pack(pady=10)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            member_id,
            name,
            phone,
            email,
            join_date
        FROM members
        ORDER BY member_id
    """)

    members = cursor.fetchall()

    connection.close()

    for member in members:
        table.insert("", tk.END, values=member)

    add_button = tk.Button(
        root,
        text="Add New Member",
        width=20,
        command=add_member
    )
    add_button.pack(pady=5)

    edit_button = tk.Button(
        root,
        text="Edit Member",
        width=20,
        command=lambda: edit_member(table)
    )
    edit_button.pack(pady=5)

    delete_button = tk.Button(
        root,
        text="Delete Member",
        width=20,
        command=lambda: delete_member(table)
    )
    delete_button.pack(pady=5)

    back_button = tk.Button(
        root,
        text="Back to Dashboard",
        width=20,
        command=show_dashboard
    )
    back_button.pack(pady=20)

def delete_member(table):

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "No Member Selected",
            "Please select a member from the list first."
        )
        return

    member = table.item(selected[0])["values"]
    member_id = member[0]
    member_name = member[1]

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM loans
        WHERE member_id = ?
        AND return_date IS NULL
    """, (member_id,))

    active_loans = cursor.fetchone()[0]
    connection.close()

    # Outstanding loans must be returned before a member can be deleted.
    if active_loans > 0:
        messagebox.showwarning(
            "Cannot Delete Member",
            f"{member_name} currently has a borrowed tool.\n"
            "Return the tool before deleting this member."
        )
        return

    confirm = messagebox.askyesno(
        "Delete Member",
        f"Are you sure you want to delete {member_name}?"
    )

    if not confirm:
        return

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM members WHERE member_id = ?",
        (member_id,)
    )

    connection.commit()
    connection.close()

    messagebox.showinfo(
        "Member Deleted",
        f"{member_name} has been deleted."
    )

    show_members()

def edit_member(table):

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "No Member Selected",
            "Please select a member from the list first."
        )
        return

    member = table.item(selected[0])["values"]

    member_id = member[0]
    name = member[1]
    phone = member[2]
    email = member[3]
    join_date = member[4]

    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(
        root,
        text="Edit Member",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    tk.Label(root, text="Name:").pack()
    name_entry = tk.Entry(root, width=35)
    name_entry.insert(0, name)
    name_entry.pack(pady=5)

    tk.Label(root, text="Phone:").pack()
    phone_entry = tk.Entry(root, width=35)
    phone_entry.insert(0, phone)
    phone_entry.pack(pady=5)

    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root, width=35)
    email_entry.insert(0, email)
    email_entry.pack(pady=5)

    tk.Label(root, text="Join Date (YYYY-MM-DD):").pack()
    join_date_entry = tk.Entry(root, width=35)
    join_date_entry.insert(0, join_date)
    join_date_entry.pack(pady=5)

    def save_changes():
        new_name = name_entry.get()
        new_phone = phone_entry.get()
        new_email = email_entry.get()
        new_join_date = join_date_entry.get()

        if not new_name or not new_phone or not new_email or not new_join_date:
                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields."
                )
                return

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("""
                UPDATE members
                SET name = ?, phone = ?, email = ?, join_date = ?
                WHERE member_id = ?
            """, (
                new_name,
                new_phone,
                new_email,
                new_join_date,
                member_id
            ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
                "Member Updated",
                "The member has been updated successfully."
            )

        show_members()

    save_button = tk.Button(
        root,
        text="Save Changes",
        width=20,
        command=save_changes
    )
    save_button.pack(pady=15)

    cancel_button = tk.Button(
        root,
        text="Cancel",
        width=20,
        command=show_members
    )
    cancel_button.pack(pady=5)


def show_borrow_tool():

    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(
        root,
        text="Borrow Tool",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT member_id, name
        FROM members
        ORDER BY name
    """)
    members = cursor.fetchall()

    cursor.execute("""
        SELECT tool_id, name
        FROM tools
        WHERE status = 'Available'
        ORDER BY name
    """)
    tools = cursor.fetchall()

    connection.close()

    tk.Label(root, text="Select Member:").pack()

    member_combo = ttk.Combobox(
        root,
        width=35,
        state="readonly"
    )

    member_combo["values"] = [
        f"{member[0]} - {member[1]}"
        for member in members
    ]

    member_combo.pack(pady=5)

    tk.Label(root, text="Select Tool:").pack()

    tool_combo = ttk.Combobox(
        root,
        width=35,
        state="readonly"
    )

    tool_combo["values"] = [
        f"{tool[0]} - {tool[1]}"
        for tool in tools
    ]

    tool_combo.pack(pady=5)

    tk.Label(root, text="Due Date (YYYY-MM-DD):").pack()

    due_date_entry = tk.Entry(
        root,
        width=38
    )
    due_date_entry.pack(pady=5)

    default_due_date = date.today() + timedelta(days=14)
    due_date_entry.insert(0, default_due_date.isoformat())

    def borrow_tool():
        member_selection = member_combo.get()
        tool_selection = tool_combo.get()
        due_date = due_date_entry.get().strip()

        if not member_selection or not tool_selection:
            messagebox.showerror(
                "Missing Information",
                "Please select both a member and a tool."
            )
            return

        member_id = int(member_selection.split(" - ")[0])
        tool_id = int(tool_selection.split(" - ")[0])

        connection = None

        try:
            connection = sqlite3.connect(DATABASE_PATH)
            cursor = connection.cursor()

            # Availability may have changed since the dropdown was loaded.
            cursor.execute("""
                SELECT status
                FROM tools
                WHERE tool_id = ?
            """, (tool_id,))

            result = cursor.fetchone()

            if result is None or result[0] != "Available":
                messagebox.showerror(
                    "Tool Unavailable",
                    "This tool is no longer available."
                )
                connection.close()
                return

            cursor.execute("""
    INSERT INTO loans
    (member_id, tool_id, loan_date, due_date)
    VALUES (?, ?, ?, ?)
""", (
    member_id,
    tool_id,
    date.today().isoformat(),
    due_date
))

            cursor.execute("""
                UPDATE tools
                SET status = 'Borrowed'
                WHERE tool_id = ?
            """, (tool_id,))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Tool Borrowed",
                "The tool has been borrowed successfully."
            )

            show_dashboard()

        except sqlite3.Error as error:
            if connection:
                connection.rollback()
                connection.close()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    borrow_button = tk.Button(
        root,
        text="Confirm Borrow",
        width=20,
        command=borrow_tool
    )
    borrow_button.pack(pady=15)

    back_button = tk.Button(
        root,
        text="Back to Dashboard",
        width=20,
        command=show_dashboard
    )
    back_button.pack(pady=5)

    member_combo.focus_set()

    member_combo.bind(
        "<Return>",
        lambda event: tool_combo.focus_set()
    )

    tool_combo.bind(
        "<Return>",
        lambda event: due_date_entry.focus_set()
    )

    due_date_entry.bind(
        "<Return>",
        lambda event: borrow_tool()
    )


def show_return_tool():

    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(
        root,
        text="Return Tool",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
    loans.loan_id,
    tools.name,
    members.name,
    loans.loan_date,
    loans.due_date
    FROM loans
    JOIN tools
    ON loans.tool_id = tools.tool_id
    JOIN members
    ON loans.member_id = members.member_id
    WHERE loans.return_date IS NULL
    ORDER BY loans.loan_id
    """)

    active_loans = cursor.fetchall()
    connection.close()

    tk.Label(
    root,
    text="Select Tool to Return:"
    ).pack(pady=5)

    loan_combo = ttk.Combobox(
    root,
    width=45,
    state="readonly"
    )

    loan_combo["values"] = [
    f"{loan[0]} - {loan[1]} - Borrowed by {loan[2]}"
    for loan in active_loans
    ]

    loan_combo.pack(pady=10)

    if not active_loans:
        loan_combo["values"] = ["No tools currently borrowed"]
        loan_combo.current(0)
        loan_combo.config(state="disabled")

    def return_tool():
        selection = loan_combo.get()

        if not selection or not active_loans:
            messagebox.showerror(
                "No Loan Selected",
                "There is no active loan to return."
            )
            return

        loan_id = int(selection.split(" - ")[0])

        connection = None

        try:
            connection = sqlite3.connect(DATABASE_PATH)
            cursor = connection.cursor()

            cursor.execute("""
                SELECT tool_id
                FROM loans
                WHERE loan_id = ?
                AND return_date IS NULL
            """, (loan_id,))

            result = cursor.fetchone()

            if result is None:
                messagebox.showerror(
                    "Return Error",
                    "This loan has already been returned."
                )
                connection.close()
                return

            tool_id = result[0]

            cursor.execute("""
                UPDATE loans
                SET return_date = ?
                WHERE loan_id = ?
            """, (
                date.today().isoformat(),
                loan_id
            ))

            cursor.execute("""
                UPDATE tools
                SET status = 'Available'
                WHERE tool_id = ?
            """, (tool_id,))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Tool Returned",
                "The tool has been returned successfully."
            )

            show_dashboard()

        except sqlite3.Error as error:
            if connection:
                connection.rollback()
                connection.close()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    return_button = tk.Button(
        root,
        text="Confirm Return",
        width=20,
        command=return_tool
    )
    return_button.pack(pady=15)

    back_button = tk.Button(
        root,
        text="Back to Dashboard",
        width=20,
        command=show_dashboard
    )
    back_button.pack(pady=5)

    loan_combo.bind(
        "<Return>",
        lambda event: return_tool()
    )

    loan_combo.focus_set()

def show_dashboard():

    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(
        root,
        text="Community Tool Library",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=30)

    subtitle = tk.Label(
        root,
        text="Management Dashboard",
        font=("Arial", 16)
    )
    subtitle.pack(pady=10)

    tools_button = tk.Button(
    root,
    text="Tools",
    width=20,
    height=2,
    command=show_tools
)
    tools_button.pack(pady=5)

    members_button = tk.Button(
    root,
    text="Members",
    width=20,
    height=2,
    command=show_members
)
    members_button.pack(pady=5)

    borrow_button = tk.Button(
    root,
    text="Borrow Tool",
    width=20,
    height=2,
    command=show_borrow_tool
)
    borrow_button.pack(pady=5)

    return_button = tk.Button(
    root,
    text="Return Tool",
    width=20,
    height=2,
    command=show_return_tool
)
    return_button.pack(pady=5)

title = tk.Label(
    root,
    text="Community Tool Library",
    font=("Arial", 22, "bold")
)
title.pack(pady=40)

login_label = tk.Label(
    root,
    text="Staff Login",
    font=("Arial", 16)
)
login_label.pack(pady=10)

username_label = tk.Label(root, text="Username:")
username_label.pack()

username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=5)

password_label = tk.Label(root, text="Password:")
password_label.pack()

password_entry = tk.Entry(
    root,
    width=30,
    show="*"
)
password_entry.pack(pady=5)

login_button = tk.Button(
    root,
    text="Login",
    width=15,
    command=login
)
login_button.pack(pady=20)

username_entry.bind(
    "<Return>",
    lambda event: password_entry.focus_set()
)

password_entry.bind(
    "<Return>",
    lambda event: login()
)

username_entry.focus_set()

root.mainloop()
