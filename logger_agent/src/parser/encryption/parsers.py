# from interface.parser_interface import ParserInterface

# class Parser(ParserInterface):
   
#    #func cleaning keys
#   def parse_data(self, keys: dict) -> dict:
    
#     new_dict = {}
#     for window, words in keys.items():
#         result = []
#         for word in words:
#             if word == 'space':  
#                 result.append(" ")   
#             elif len(word) > 1:
#                 result.append(f"<{word}>")  
#             else:
#                 result.append(word)  

#         if result:  
#             new_dict[window] = ''.join(result).strip()  

#     return new_dict  


from interface.parser_interface import ParserInterface

class Parser(ParserInterface):
    def parse_data(self, buffer):
        """parser buffer."""
        return self.clean_and_join(buffer)
    
    
    def clean_and_join(self, keys: dict) -> dict:
        unwanted_keys = {"ctrl", "left", "right", "right shift","left shift", "alt", "tab", "backspace"}
        
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