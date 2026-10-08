import sqlite3

def generate_user_report(conn: sqlite3.Connection):
    """
    Generates a text report containing all users and their associated recent orders.
    """
    cursor = conn.cursor()
    
    # Fetch all users (Missing Pagination)
    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()
    
    report_lines = ["--- USER REPORT ---"]
    
    # N+1 Query Problem: We are executing a separate query inside a loop for each user.
    for user_id, user_name in users:
        cursor.execute("SELECT order_total, order_date FROM orders WHERE user_id = ?", (user_id,))
        orders = cursor.fetchall()
        
        report_lines.append(f"User: {user_name}")
        for total, date in orders:
            report_lines.append(f"  - Order on {date} for ${total}")
            
    return "\n".join(report_lines)
