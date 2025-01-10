from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database Setup
DATABASE = "banking_system.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            account_type TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(account_id) REFERENCES accounts(id)
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Routes
@app.route('/register', methods=['POST'])
def register_customer():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, email, password) VALUES (?, ?, ?)",
                       (name, email, password))
        conn.commit()
        return jsonify({"message": "Customer registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    customer_id = data.get('customer_id')
    account_type = data.get('account_type')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (customer_id, account_type) VALUES (?, ?)",
                   (customer_id, account_type))
    conn.commit()
    account_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Account created successfully!", "account_id": account_id}), 201

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    account_id = data.get('account_id')
    amount = data.get('amount')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)",
                   (account_id, amount))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deposit successful!"}), 200

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    account_id = data.get('account_id')
    amount = data.get('amount')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    balance = cursor.fetchone()

    if balance and balance[0] >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdraw', ?)",
                       (account_id, amount))
        conn.commit()
        conn.close()
        return jsonify({"message": "Withdrawal successful!"}), 200
    else:
        conn.close()
        return jsonify({"error": "Insufficient balance"}), 400

# Run the server
if __name__ == "__main__":
    app.run(debug=True)
