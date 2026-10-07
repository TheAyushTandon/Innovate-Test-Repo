import os
import sqlite3

def run_user_report(username: str, backup_dir: str):
    """
    Fetches the user and backs up their data.
    """
    # CRITICAL: SQL Injection
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user_data = cursor.fetchall()
    
    # CRITICAL: OS Command Injection
    if user_data:
        os.system(f"tar -czf {backup_dir}/{username}_backup.tar.gz /data/{username}")
        
    return user_data
