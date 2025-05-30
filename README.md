# py-crypt-sindresorhus-conf

This Python library encrypts/decrypts [`sindresorhus/conf`](https://github.com/sindresorhus/conf) and [`sindresorhus/electron-store`](https://github.com/sindresorhus/electron-store) files.

## Installation
```bash
# cryptography
pip install "crypt_sindresorhus_conf[cryptography] @ git+https://github.com/DimmaDont/py-crypt-sindresorhus-conf"

# PyCryptodome
pip install "crypt_sindresorhus_conf[pycryptodome] @ git+https://github.com/DimmaDont/py-crypt-sindresorhus-conf"
```

## Usage example
#### Encryption
```python
import json
import os

from crypt_sindresorhus_conf import CryptSindresorhusConf

key = b"hello there"
iv = os.urandom(16)
conf_crypt = CryptSindresorhusConf(key, iv)
encrypted = conf_crypt.encrypt(json.dumps({"foo": "bar"}))
```
#### Decryption
```python
import json

from crypt_sindresorhus_conf import CryptSindresorhusConf

with open("file.json", "rb") as f:
    encrypted = f.read()

key = b"hello there"
iv = encrypted[:16]
conf_crypt = CryptSindresorhusConf(key, iv)
plaintext = conf_crypt.decrypt(encrypted)
data = json.loads(plaintext)
```
