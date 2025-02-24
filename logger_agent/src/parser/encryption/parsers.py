from interface.parser_interface import ParserInterface

class Parser(ParserInterface):
   
   def clean_and_join(self, keys: list) -> str:
        unwanted_keys = {"ctrl", "enter", "left", "right", "shift", "alt", "tab", "backspace"}
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZאבגדהוזחטיכלמנסעפצקרשתםןףךץ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        
        result = []
        
        for k in keys:
            if k.lower() not in unwanted_keys and k in allowed_chars:
                result.append(k)
            elif k == 'space':
                result.append(" ")  
        
        return "".join(result)
