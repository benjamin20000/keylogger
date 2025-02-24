from interface.parser_interface import ParserInterface

class Parser(ParserInterface):
   
   def parse_data(self, keys: list) -> str:        
        result = []
        for key in keys:
            if len(key) == 1:
                result.append(key)
            elif key == 'space':
                result.append(" ")
            else:
                result.append(f"<{key}>")
        return "".join(result)
