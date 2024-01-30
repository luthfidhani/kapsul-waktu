import hashlib
from cryptography.fernet import Fernet
from datetime import datetime


def encrypt_message(message):
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)
    encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
    return encrypted_message.decode("utf-8"), encryption_key.decode("utf-8")


def decrypt_message(encrypted_message, encryption_key):
    cipher_suite = Fernet(encryption_key)
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
    return decrypted_message


def calculate_hash(message):
    sha256_hash = hashlib.sha256(message).hexdigest()
    return sha256_hash[:8]


def expiration_date_check(expiration_date):
    date_now = datetime.now()
    expiration_date_obj = datetime.strptime(expiration_date, "%d-%m-%Y")
    return date_now >= expiration_date_obj
