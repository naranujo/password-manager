import os
import json
from datetime import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend


class Passgen:
    def __init__(self, longitud: int = 16) -> None:
        """
        Constructor

        Args:
            longitud (int, optional): Password length. Defaults to 16.
        """
        if not isinstance(longitud, int):
            raise ValueError("The length arg must be an integer")
        self.longitud = longitud

    def _derive_key(self, master_key: bytes, salt: bytes, length: int = 32) -> bytes:
        """
        Generate a key derived from the master key

        Args:
            master_key (bytes): Master key
            salt (bytes): Salt
            length (int, optional): Key length. Defaults to 32.

        Returns:
            bytes: Derived key
        """
        kdf = Scrypt(
            salt=salt,
            length=length,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )
        return kdf.derive(master_key)

    def _encrypt(self, data: str, key: bytes) -> str:
        """
        Encrypt data

        Args:
            data (str): Data to encrypt
            key (bytes): Key

        Returns:
            str: Encrypted data
        """
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return urlsafe_b64encode(iv + ciphertext).decode()

    def _decrypt(self, token: str, key: bytes) -> str:
        """
        Decrypt data

        Args:
            token (str): Encrypted data
            key (bytes): Key

        Returns:
            str: Decrypted data
        """
        try:
            token = urlsafe_b64decode(token.encode())
            iv = token[:16]
            ciphertext = token[16:]
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = PKCS7(algorithms.AES.block_size).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            return data.decode(errors='ignore')
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None

    def load_passwords(self, filename: str) -> dict:
        """
        Load passwords from a file

        Args:
            filename (str): File name

        Returns:
            dict: Passwords
        """
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_passwords(self, filename: str, passwords: dict) -> None:
        """
        Save passwords to a file

        Args:
            filename (str): File name
            passwords (dict): Passwords
        """
        with open(filename, 'w') as f:
            json.dump(passwords, f, indent=4, sort_keys=False)

    def add_password(self, filename: str, service: str, username: str, password: str, master_key: str) -> None:
        """
        Add a password

        Args:
            filename (str): File name
            service (str): Service
            username (str): Username
            password (str): Password
            master_key (str): Master key
        """
        master_key_bytes = master_key.encode('utf-8')
        passwords = self.load_passwords(filename)

        if service in passwords:
            salt = urlsafe_b64decode(passwords[service]['salt'])
            key = self._derive_key(master_key_bytes, salt)
            decrypted_username = self._decrypt(passwords[service]['username'], key)
            if decrypted_username == username:
                if self._decrypt(passwords[service]['password'], key) != password:
                    print("Updating password")
                    passwords[service]['password'] = self._encrypt(password, key)
                    passwords[service]['updated_at'] = datetime.now().isoformat()
                    self._save_passwords(filename, passwords)
                else:
                    print("The new password is the same as the old password.")
            else:
                print("Service already exists with a different username.")
        else:
            salt = os.urandom(16)
            key = self._derive_key(master_key_bytes, salt)
            passwords[service] = {
                'username': self._encrypt(username, key),
                'password': self._encrypt(password, key),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'salt': urlsafe_b64encode(salt).decode(),
            }
            self._save_passwords(filename, passwords)

    def get_password(self, filename: str, service: str, master_key: str) -> dict:
        """
        Get a password

        Args:
            filename (str): File name
            service (str): Service
            master_key (str): Master key

        Returns:
            dict | None: Password details or None
        """
        master_key_bytes = master_key.encode('utf-8')
        passwords = self.load_passwords(filename)
        if service in passwords:
            salt = urlsafe_b64decode(passwords[service]['salt'])
            key = self._derive_key(master_key_bytes, salt)
            decrypted_username = self._decrypt(passwords[service]['username'], key)
            if decrypted_username:
                return {
                    'username': decrypted_username,
                    'password': self._decrypt(passwords[service]['password'], key)
                }
        return None

    def check_master_key(self, filename: str, master_key: str) -> bool:
        """
        Check master key

        Args:
            filename (str): File name
            master_key (str): Master key

        Returns:
            bool: True if the master key is correct, False otherwise
        """
        master_key_bytes = master_key.encode('utf-8')
        passwords = self.load_passwords(filename)
        for service in passwords:
            salt = urlsafe_b64decode(passwords[service]['salt'])
            key = self._derive_key(master_key_bytes, salt)
            if not self._decrypt(passwords[service]['username'], key):
                return False
        return True
