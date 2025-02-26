from interface.encrypt_interface import EncryptInteface

class Xor(EncryptInteface):
    def __init__(self, key="my_secret_key"):
        self.key = key

   

    def encrypt(self, data: dict) -> dict:
        print("Data before encryption:", data)  
    
        encrypted_data = {}
        for window, text in data.items():  
            encrypted_text = "".join(chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(text))
            encrypted_data[window] = encrypted_text  

        print("Data after encryption:", encrypted_data)  
        return encrypted_data
 



