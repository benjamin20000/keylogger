from interface.parser_interface import ParserInterface

class Parser(ParserInterface):
   
   #func cleaning keys
  def parse_data(self, keys: dict) -> dict:
    
    new_dict = {}
    for window, words in keys.items():
        result = []
        for word in words:
            if word == 'space':  
                result.append(" ")   
            elif len(word) > 1:
                result.append(f"<{word}>")  
            else:
                result.append(word)  

        if result:  
            new_dict[window] = ''.join(result).strip()  

    return new_dict  
