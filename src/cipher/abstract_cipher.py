"""
Abstract Cipher class
"""

from abc import ABC, abstractmethod


class Cipher(ABC):
    """
    Cipher abstract class
    """

    @abstractmethod
    def encrypt(self, raw: bytes) -> bytes:
        """
        Encrypt raw data

        paramaters
        ----------
        raw: bytes
            Raw data

        returns
        -------
        bytes
            Encrypted data
        """

    @abstractmethod
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
