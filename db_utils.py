import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'expense.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the SQLite database if it doesn't exist."""
    if os.path.exists(DB_PATH):
        print('Database already exists at', DB_PATH)
        return

    print('Creating new database at', DB_PATH)
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_budget REAL DEFAULT 20000
            )
        ''')

        # Insert default settings row
        cur.execute('INSERT INTO settings (total_budget) VALUES (?)', (20000,))
        conn.commit()
        print('Initialized database with tables and default settings.')
    except Exception as e:
        print('Error initializing database:', e)
    finally:
        conn.close()


# Utility functions
def fetch_expenses():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM expenses ORDER BY date DESC')
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def fetch_expense(expense_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM expenses WHERE id=?', (expense_id,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def add_expense(title, amount, category, date_str):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO expenses (title, amount, category, date) VALUES (?,?,?,?)',
                    (title, amount, category, date_str))
        conn.commit()
        print('Expense added:', title, amount)
        return cur.lastrowid
    except Exception as e:
        print('Error adding expense:', e)
        return None
    finally:
        conn.close()


def update_expense(expense_id, title, amount, category, date_str):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('UPDATE expenses SET title=?, amount=?, category=?, date=? WHERE id=?',
                    (title, amount, category, date_str, expense_id))
        conn.commit()
        print('Expense updated:', expense_id)
        return True
    except Exception as e:
        print('Error updating expense:', e)
        return False
    finally:
        conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM expenses WHERE id=?', (expense_id,))
        conn.commit()
        print('Expense deleted:', expense_id)
        return True
    except Exception as e:
        print('Error deleting expense:', e)
        return False
    finally:
        conn.close()


def get_settings():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM settings LIMIT 1')
        row = cur.fetchone()
        if row:
            return dict(row)
        return {'total_budget': 20000}
    finally:
        conn.close()


def update_budget(new_budget):
    conn = get_connection()
    try:
        cur = conn.cursor()
        # If there is a settings row, update it; otherwise insert
        cur.execute('SELECT id FROM settings LIMIT 1')
        row = cur.fetchone()
        if row:
            cur.execute('UPDATE settings SET total_budget=? WHERE id=?', (new_budget, row['id']))
        else:
            cur.execute('INSERT INTO settings (total_budget) VALUES (?)', (new_budget,))
        conn.commit()
        print('Budget updated to', new_budget)
        return True
    except Exception as e:
        print('Error updating budget:', e)
        return False
    finally:
        conn.close()


def totals_summary():
    """Return computed totals: total, monthly, highest, used"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT SUM(amount) as total FROM expenses')
        total_row = cur.fetchone()
        total = total_row['total'] or 0

        # Monthly total (current month)
        now = datetime.now()
        month_prefix = now.strftime('%Y-%m')
        cur.execute("SELECT SUM(amount) as monthly FROM expenses WHERE date LIKE ?", (month_prefix + '%',))
        monthly_row = cur.fetchone()
        monthly = monthly_row['monthly'] or 0

        cur.execute('SELECT MAX(amount) as highest FROM expenses')
        highest_row = cur.fetchone()
        highest = highest_row['highest'] or 0

        settings = get_settings()
        budget = settings.get('total_budget', 20000)
        used = total
        remaining = budget - used

        return {'total': total, 'monthly': monthly, 'highest': highest, 'budget': budget, 'used': used, 'remaining': remaining}
    finally:
        conn.close()
