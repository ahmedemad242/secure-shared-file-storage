"""
Blowfish cipher
"""

from Cryptodome.Cipher import Blowfish

from .abstract_cipher import Cipher


class BlowfishCipher(Cipher):
    """
    Blowfish cipher class
    """

    def __init__(self, key: bytes) -> None:
        self.key = key
        self.cipher = Blowfish.new(self.key, Blowfish.MODE_ECB)

    def setKey(self, key: bytes) -> None:
        """
        Set key

        paramaters
        ----------
        key: bytes
            Key
        """

        self.key = key
        self.cipher = Blowfish.new(self.key, Blowfish.MODE_ECB)

    def encrypt(self, raw: bytes) -> bytes:
        """
        Encrypt raw data using Blowfish

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
