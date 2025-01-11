import json
import os
import subprocess
import unittest

from src.crypt_sindresorhus_conf import CryptSindresorhusConf


class TestCryptSindresorhusConf(unittest.TestCase):
    def setUp(self):
        subprocess.run(["node", "tests/main.mjs"], check=True)

        with open("key.txt", "rb") as f:
            key = f.read()

        with open("config.json", "rb") as f:
            self.encrypted = f.read()

        with open("config_plaintext.json", "rb") as f:
            self.plaintext = f.read()

        iv = self.encrypted[:16]
        self.crypt = CryptSindresorhusConf(key, iv)

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

    def tearDown(self):
        os.remove("key.txt")
        os.remove("config.json")
        os.remove("config_plaintext.json")
