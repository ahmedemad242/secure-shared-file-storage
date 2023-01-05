"""
RSA Cipher
"""

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

from .abstract_cipher import Cipher


class RSACipher(Cipher):
    """
    RSA cipher class
    """

    def __init__(self, key: bytes) -> None:
        self.key = RSA.import_key(key)
        self.cipher = PKCS1_OAEP.new(self.key)

    def setKey(self, key: bytes) -> None:
        """
        Set key

        paramaters
        ----------
        key: bytes
            Key
        """

        self.key = RSA.import_key(key)
        self.cipher = PKCS1_OAEP.new(self.key)

    def encrypt(self, raw: bytes) -> bytes:
        """
        Encrypt raw data using RSA

        paramaters
        ----------
        raw: bytes
            Raw data

        returns
        -------
        bytes
            Encrypted data
        """

        return self.cipher.encrypt(raw)

    def decrypt(self, enc: bytes) -> bytes:
        """
        Decrypt encrypted data

        paramaters
        ----------
        enc: bytes
            Encrypted data

        returns
        -------
        bytes
            Decrypted data
        """

        return self.cipher.decrypt(enc)
