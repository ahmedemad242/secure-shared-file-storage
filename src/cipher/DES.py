"""
DES cipher module
"""

from Cryptodome.Cipher import DES

from .abstract_cipher import Cipher


class DESCipher(Cipher):
    """
    DES cipher class
    """

    def __init__(self, key: bytes) -> None:
        self.key = key
        self.cipher = DES.new(self.key, DES.MODE_OFB)

    def setKey(self, key: bytes) -> None:
        """
        Set key

        paramaters
        ----------
        key: bytes
            Key
        """

        self.key = key
        self.cipher = DES.new(self.key, DES.MODE_ECB)

    def encrypt(self, raw: bytes) -> bytes:
        """
        Encrypt raw data using DES

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
