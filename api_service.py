import sqlite3
import subprocess

API_KEY = "AKIA1234567890EXAMPLEKEY"  # Secret leak

def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

def ping_host(host):
    # Command Injection vulnerability
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return result.decode()

def calculate_discount(price, discount_code):
    # Division by zero & unhandled error
    rates = {"HALF": 2, "FREE": 0}
    divisor = rates.get(discount_code, 1)
    return price / divisor
