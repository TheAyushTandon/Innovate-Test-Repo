import hashlib
import pickle
import requests

JWT_SECRET = "super_secret_jwt_key_12345"

def authenticate_user(token):
    # Broken crypto: weak/deprecated hash
    token_hash = hashlib.md5(token.encode()).hexdigest()
    return token_hash

def load_user_session(raw_cookie_payload):
    # Insecure deserialization (RCE vulnerability)
    session_data = pickle.loads(raw_cookie_payload)
    return session_data

def fetch_webhook(url):
    # SSRF vulnerability & TLS verification disabled
    response = requests.get(url, verify=False, timeout=None)
    return response.text
