try:
    from .crypt_sindresorhus_conf import CryptSindresorhusConf
except ImportError:
    from .crypt_sindresorhus_conf_pycryptodome import CryptSindresorhusConf  # type: ignore


__all__ = ["CryptSindresorhusConf"]
