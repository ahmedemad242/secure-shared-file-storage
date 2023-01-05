"""
FileEncrypter module.
"""

from src.cipher.hybrid_cipher import HybridEncrypter
from src.cipher.RSA import RSACipher


class FileCryptographer:
    """
    This class is used to encrypt a file using a key.
    """

    @staticmethod
    def encryptFile(fileName: str, publicKey: bytes) -> None:
        """
        Encrypts a file using a key.

        parameters
        ----------
        fileName: str
            Path to the file to be encrypted
        publicKey: bytes
            Key used to encrypt the file
        """

        try:
            with open(fileName, "rb") as file:
                raw = file.read()

            encrypted, keys = HybridEncrypter.encrypt(raw)
            rsaCipher = RSACipher(publicKey)
            encryptedKeys = rsaCipher.encrypt(keys)

            with open(fileName + ".enc", "wb") as file:
                file.write(encrypted)

            with open(fileName + ".key", "wb") as file:
                file.write(keys)

            with open(fileName + ".key.enc", "wb") as file:
                file.write(encryptedKeys)

        except FileNotFoundError as exp:
            raise FileNotFoundError("File not found") from exp

    @staticmethod
    def decryptFile(fileName: str, privateKey: bytes) -> None:
        """
        Decrypts a file using a key.

        parameters
        ----------
        fileName: str
            Path to the file to be decrypted
        key: bytes
            Key used to decrypt the file
        """

        try:
            with open(fileName + ".enc", "rb") as file:
                encrypted = file.read()

            with open(fileName + ".key.enc", "rb") as file:
                encryptedKeys = file.read()

            rsaCipher = RSACipher(privateKey)
            keys = rsaCipher.decrypt(encryptedKeys)

            decrypted = HybridEncrypter.decrypt(encrypted, keys)

            with open(fileName + ".dec", "wb") as file:
                file.write(decrypted)

        except FileNotFoundError as exp:
            raise FileNotFoundError("File not found") from exp
