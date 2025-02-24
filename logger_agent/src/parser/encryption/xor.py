from interface.encrypt_interface import EncryptInteface

class Xor(EncryptInteface):
    def __init__(self, key="my_secret_key"):
        self.key = key

    def encrypt(self, data: str) -> str:
        return "".join(chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(data))