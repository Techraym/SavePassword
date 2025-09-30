"""
Encryption and decryption utilities
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class CryptoManager:
    """Manage encryption and decryption"""
    
    def __init__(self):
        self.key = None
        self.fernet = None
    
    def set_key_from_password(self, password, salt=None):
        """Set encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(key)
        return salt
    
    def encrypt(self, data):
        """Encrypt data"""
        if self.fernet and data:
            return self.fernet.encrypt(data.encode())
        return data.encode() if data else b''
    
    def decrypt(self, encrypted_data):
        """Decrypt data"""
        if self.fernet and encrypted_data:
            return self.fernet.decrypt(encrypted_data).decode()
        return encrypted_data.decode() if encrypted_data else ''