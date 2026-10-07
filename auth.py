import hashlib

def hash_password(password: str) -> str:
    """
    Hashes a password for storage.
    """
    # Security Flaw: Using MD5, which is cryptographically broken and vulnerable to collision attacks.
    return hashlib.md5(password.encode('utf-8')).hexdigest()
