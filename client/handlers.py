#import ...

def make_indents(s: str, chars_in_line: int = 32) -> str:
    output = ""
    chars_count = 0
    
    for index in s.split():
        if chars_count > chars_in_line:
            output += "\n"
            chars_count = 0
            
        output += index + " "
        chars_count += len(index)
        
    return output
