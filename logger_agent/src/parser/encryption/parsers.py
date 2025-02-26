from interface.parser_interface import ParserInterface

class Parser(ParserInterface):
   
   #func cleaning keys
  def clean_and_join(self, keys: dict) -> dict:

    unwanted_keys = {"ctrl", "left", "right", "shift", "alt", "tab", "backspace"}
    
    new_dict = {}
    for window, words in keys.items():
        result = []
        for word in words:
            if word.lower() in unwanted_keys:  
                continue  
            elif word == 'space':
                result.append(" ")  
            elif word == 'enter':
                result.append("[enter]") 
            elif word == 'delete':
                result.append("[delete]")  
            else:
                result.append(word)  

        if result:  
            new_dict[window] = ''.join(result).strip()  

    return new_dict  


