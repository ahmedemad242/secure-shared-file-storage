"""
AES cipher module
"""

from Cryptodome.Cipher import AES

from .abstract_cipher import Cipher


class AESCipher(Cipher):
    """
    AES cipher class
    """

    def __init__(self, key: bytes) -> None:
        self.key = key
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def setKey(self, key: bytes) -> None:
        """
        Set key

        paramaters
        ----------
        key: bytes
            Key
        """

        self.key = key
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, raw: bytes) -> bytes:
        """
        Encrypt raw data using AES

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
