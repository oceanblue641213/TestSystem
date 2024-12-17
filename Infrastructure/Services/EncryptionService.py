from cryptography.fernet import Fernet

class EncryptionService:
    @staticmethod
    def encrypt_sensitive_data(data):
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data, key

    @staticmethod
    def decrypt_sensitive_data(encrypted_data, key):
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data).decode()
        return decrypted_data