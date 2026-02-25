from cryptography.fernet import Fernet
key = Fernet.generate_key()
print("Copy this entire line:")
print(f'KEY = {key!r}')  # Output: KEY = b'gAAAAABk...'
