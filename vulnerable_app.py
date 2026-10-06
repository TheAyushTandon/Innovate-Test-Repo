import os
import sqlite3
import pickle
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# FATAL 1: Hardcoded secrets and API keys
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"
JWT_SECRET = "super_secret_key_123"

# FATAL 2: Database connection as global state (thread-unsafe if multithreaded)
# And using an insecure temp db
db_conn = sqlite3.connect("users.db")
db_conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, role TEXT)")
db_conn.execute("INSERT INTO users VALUES (1, 'admin', 'admin')")
db_conn.commit()

class VulnerableServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # FATAL 3: Path Traversal Vulnerability
        if parsed_path.path.startswith("/files/"):
            filename = parsed_path.path.replace("/files/", "")
            # No sanitization, allowing "../../../etc/passwd"
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(str(e).encode())
            return

        # FATAL 4: SQL Injection
        if parsed_path.path.startswith("/users/"):
            user_id = parsed_path.path.replace("/users/", "")
            cursor = db_conn.cursor()
            # String formatting used directly in SQL query!
            query = f"SELECT name, role FROM users WHERE id = {user_id}"
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(str(results).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
            return
            
        # FATAL 5: Unbounded infinite loop / Denial of Service
        if parsed_path.path.startswith("/sync"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Starting sync...")
            # Thread starvation / CPU Hog
            retry_count = 0
            while True:
                # Simulating a failed connection with no breakout condition
                if retry_count < 0:
                    break
                retry_count += 1
            return
            
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # FATAL 6: Insecure Deserialization (Pickle)
        if parsed_path.path == "/upload_session":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Malicious payloads can execute arbitrary code upon unpickling
                session_data = pickle.loads(post_data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Session loaded: {session_data}".encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
            return

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8080), VulnerableServer)
    print("Running vulnerable server on port 8080...")
    server.serve_forever()
