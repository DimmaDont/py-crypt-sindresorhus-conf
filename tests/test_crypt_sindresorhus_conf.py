import json
import os
import subprocess
import unittest

from src.crypt_sindresorhus_conf import CryptSindresorhusConf


class TestReadConf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(["node", "tests/conf_write.mjs"], check=True)

        with open("key.txt", "rb") as f:
            key = f.read()

        with open("config.json", "rb") as f:
            cls.encrypted = f.read()

        with open("config_plaintext.json", "rb") as f:
            cls.plaintext = f.read()

        iv = cls.encrypted[:16]
        cls.crypt = CryptSindresorhusConf(key, iv)

    def test_decrypt(self):
        decrypted = self.crypt.decrypt(self.encrypted)
        self.assertEqual(decrypted, self.plaintext)

    def test_encrypt(self):
        encrypted = self.crypt.encrypt(self.plaintext)
        self.assertEqual(encrypted, self.encrypted)

    def test_json(self):
        data = json.loads(self.plaintext)
        self.assertEqual(data["c"], 1)
        self.assertEqual(data["b"], 2)
        self.assertEqual(data["a"], 3)

    @classmethod
    def tearDownClass(cls):
        os.remove("key.txt")
        os.remove("config.json")
        os.remove("config_plaintext.json")


class TestWriteConf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        key = b"ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"

        with open("key.txt", "wb") as f:
            f.write(key)

        iv = os.urandom(16)
        crypt = CryptSindresorhusConf(key, iv)

        cls.plaintext = json.dumps({"x": 4, "y": 5, "z": 6}, indent="\t").encode()
        encrypted = crypt.encrypt(cls.plaintext)

        with open("config.json", "wb") as f:
            f.write(encrypted)

    def test_readable_by_conf(self):
        subprocess.run(["node", "tests/conf_read.mjs"], check=True)
        with open("config_plaintext.json", "rb") as f:
            plaintext = f.read()
        self.assertEqual(plaintext, self.plaintext)

    @classmethod
    def tearDownClass(cls):
        os.remove("key.txt")
        os.remove("config.json")
        os.remove("config_plaintext.json")
