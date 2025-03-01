import logging

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.padding import PKCS7


logger = logging.getLogger("crypt_sindresorhus_conf")


class CryptSindresorhusConf:
    def __init__(self, key: bytes, iv: bytes):
        self.iv = iv
        logger.debug("Key:      %d %s", len(key), key.hex())
        logger.debug("IV:       %d %s", len(iv), iv.hex())

        # js: `iv.toString()` ...
        salt = iv.decode(encoding="utf-8", errors="replace").encode()
        logger.debug("Salt:     %d %s", len(salt), salt.hex())

        kdf = PBKDF2HMAC(algorithm=SHA512(), length=32, salt=salt, iterations=10_000)
        self.password = kdf.derive(key)
        logger.debug("Password: %d %s", len(self.password), self.password.hex())

        self.cipher = Cipher(AES(self.password), CBC(iv))

    def encrypt(self, data: bytes) -> bytes:
        padder = PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        encryptor = self.cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return self.iv + b":" + encrypted

    def decrypt(self, data: bytes) -> bytes:
        decryptor = self.cipher.decryptor()
        # iv and data are separated by a ":"
        decrypted = decryptor.update(data[17:]) + decryptor.finalize()
        unpadder = PKCS7(128).unpadder()
        unpadded = unpadder.update(decrypted) + unpadder.finalize()
        return unpadded
