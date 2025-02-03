import sqlite3
from datetime import datetime

def connect_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT,
                        amount REAL,
                        category TEXT,
                        date TEXT)''')
    conn.commit()
    return conn

def add_transaction(conn, trans_type, amount, category):
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)",
                   (trans_type, amount, category, date))
    conn.commit()
    print(f"{trans_type.capitalize()} of {amount} added under {category} category.")

def view_summary(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    summary = cursor.fetchall()
    
    income = 0
    expenses = 0
    for item in summary:
        if item[0] == "income":
            income = item[1]
        elif item[0] == "expense":
            expenses = item[1]
    
    savings = income - expenses
    print("\n--- Monthly Summary ---")
    print(f"Total Income: {income}")
    print(f"Total Expenses: {expenses}")
    print(f"Savings: {savings}\n")

def main():
    conn = connect_db()
    while True:
        print("\n1. Add Income\n2. Add Expense\n3. View Summary\n4. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            amount = float(input("Enter income amount: "))
            category = input("Enter category: ")
            add_transaction(conn, "income", amount, category)
        elif choice == "2":
            amount = float(input("Enter expense amount: "))
            category = input("Enter category: ")
            add_transaction(conn, "expense", amount, category)
        elif choice == "3":
            view_summary(conn)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")
    
    conn.close()

if __name__ == "__main__":
    main()
