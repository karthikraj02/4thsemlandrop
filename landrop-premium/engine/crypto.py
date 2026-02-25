from cryptography.fernet import Fernet

# Fixed shared key - SAME on ALL machines!
KEY = b'lH1g7NTviFJpFX1TkhqpQqCDR1KuFw-bv7oJuSEcAsU='  # Simple 44-char key for testing

cipher_suite = Fernet(KEY)

def encrypt(data):
    """Encrypt bytes data using Fernet (AES-128)"""
    return cipher_suite.encrypt(data)

def decrypt(data):
    """Decrypt bytes data using same Fernet key"""
    return cipher_suite.decrypt(data)
