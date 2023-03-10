"""
Hybrid encrypter class
The following methodology is followed for encryption:
    1.  Dividing the file to upload into N parts. each one is 16 bytes long.
    2.  Generate 3 keys randomly, for AES, Blowfish and DES
    3.  Encrypting all the parts of the file using the three algorithms in round robin fashion.
        And the parts are put together in a single file as ordered.
    4.  The keys for cryptography algorithms are then grouped in a key file

The decryption follows the same methodology is reverse order
"""

from typing import Tuple, List, Generator
from Cryptodome.Random import get_random_bytes

from .AES import AESCipher
from .DES import DESCipher
from .blowfish import BlowfishCipher
from .abstract_cipher import Cipher


def roundRobinCipher(ciphers: List[Cipher]) -> Generator[Cipher, None, None]:
    """
    Round robin cipher

    paramaters
    ----------
    ciphers: List[Cipher]
        List of ciphers

    returns
    -------
    Generator[Cipher, None, None]
        Generator of ciphers which yields a cipher in round robin fashion
    """

    while True:
        for cipher in ciphers:
            yield cipher


class HybridEncrypter:
    """
    Hybrid encrypter class
    """

    @staticmethod
    def encrypt(raw: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypt raw data using hybrid encryption

        paramaters
        ----------
        raw: bytes
            Raw data

        returns
        -------
        Tuple[bytes, bytes]
            Encrypted data and keys used for encyption (AES key (16 bytes)
            + Blowfish key (16 bytes) + DES key (8 bytes))
        """

        chunckSize = 16

        keyAes = get_random_bytes(16)
        keyBlowfish = get_random_bytes(16)
        keyDes = get_random_bytes(8)

        aes = AESCipher(keyAes)
        des = DESCipher(keyDes)
        blowfish = BlowfishCipher(keyBlowfish)

        cipherGenetator = roundRobinCipher([aes, des, des, blowfish, blowfish])

        if len(raw) % chunckSize != 0:
            raw += b" " * (chunckSize - len(raw) % chunckSize)

        currChunck = 0
        encryptedData = b""

        while True:
            chunk = raw[currChunck : currChunck + chunckSize]
            currChunck += chunckSize

            if len(chunk) == 0:
                break
            if len(chunk) % 16 != chunckSize:
                chunk += b" " * (chunckSize - len(chunk))

            encryptedData += next(cipherGenetator).encrypt(chunk)

        return (encryptedData, keyAes + keyBlowfish + keyDes)

    @staticmethod
    def decrypt(encryptedData: bytes, keys: bytes) -> bytes:
        """
        Decrypt encrypted data

        paramaters
        ----------
        enc: bytes
            Encrypted data
        keys: bytes
            Keys used for encryption (AES key (16 bytes)
            + Blowfish key (16 bytes) + DES key (8 bytes))

        returns
        -------
        bytes
            Decrypted data
        """

        chunckSize = 16

        keyAes = keys[:16]
        keyBlowfish = keys[16:32]
        keyDes = keys[32:]

        aes = AESCipher(keyAes)
        des = DESCipher(keyDes)
        blowfish = BlowfishCipher(keyBlowfish)

        cipherGenetator = roundRobinCipher([aes, des, des, blowfish, blowfish])

        if len(encryptedData) % chunckSize != 0:
            encryptedData += b" " * (chunckSize - len(encryptedData) % chunckSize)

        currChunck = 0
        decryptedData = b""

        while True:
            chunk = encryptedData[currChunck : currChunck + chunckSize]
            currChunck += chunckSize
            if len(chunk) == 0:
                break
            if len(chunk) % 16 != chunckSize:
                chunk += b" " * (chunckSize - len(chunk))

            decryptedData += next(cipherGenetator).decrypt(chunk)
            # remove padding
            decryptedData = decryptedData.rstrip()

        return decryptedData
