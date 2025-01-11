import logging

from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2


class CryptSindresorhusConf:
    def __init__(self, key: bytes, iv: bytes):
        self.iv = iv
        logging.debug("Key:      %d %s", len(key), key.hex())
        logging.debug("IV:       %d %s", len(iv), iv.hex())

        # js: `iv.toString()` ...
        salt = iv.decode(encoding="utf-8", errors="replace").encode()
        logging.debug("Salt:     %d %s", len(salt), salt.hex())

        self.password = PBKDF2(
            key.decode(), salt, 32, count=10_000, hmac_hash_module=SHA512
        )
        logging.debug("Password: %d %s", len(self.password), self.password.hex())

    def encrypt(self, data: bytes) -> bytes:
        cipher = AES.new(self.password, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(pad(data, 16))
        return self.iv + b":" + encrypted

    def decrypt(self, data: bytes) -> bytes:
        cipher = AES.new(self.password, AES.MODE_CBC, self.iv)
        # iv and data are separated by a ":"
        decrypted = cipher.decrypt(data[16 + 1 :])
        return unpad(decrypted, 16)
