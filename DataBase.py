import sqlite3

def create_db():
    conn = sqlite3.connect('Clients.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        user_id TEXT NOT NULL UNIQUE,
        phone_number TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL
    )
    ''')
    conn.commit()

def add_user(full_name, user_id, phone_number, appointment_date, appointment_time):
    conn = sqlite3.connect('Clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()
    cursor.execute('''
    INSERT INTO users (full_name, user_id, phone_number, appointment_date, appointment_time)
    VALUES (?, ?, ?, ?, ?)
    ''', (full_name, user_id, phone_number, appointment_date, appointment_time))
    conn.commit()

# Function to update an existing user's information
def update_user(full_name, user_id, phone_number, appointment_date, appointment_time):
    conn = sqlite3.connect('Clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute('''
        UPDATE users
        SET full_name = ?, phone_number = ?, appointment_date = ?, appointment_time = ?
        WHERE user_id = ?
        ''', (full_name, phone_number, appointment_date, appointment_time, user_id))
        conn.commit()
    else:
        add_user(full_name, user_id, phone_number, appointment_date, appointment_time)

def delete_user(user_id):
    conn = sqlite3.connect('Clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
    else:
        print(f"No user found with ID {user_id}.")


