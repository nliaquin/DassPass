from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64

def set_key(password):
    password = password.encode()
    salt = b'\xa1;\x93\xf4Oo=\xaf?\x9d\xc4\xc1V9\xbe\xf8'

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))

    global crypto_service
    crypto_service = Fernet(key)

def encrypt(data_string):
    encrypted_data_string = crypto_service.encrypt(data_string.encode())
    return encrypted_data_string


def decrypt(data_string):
    decrypted_data_string = crypto_service.decrypt(data_string)
    return decrypted_data_string.decode()