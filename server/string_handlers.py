from typing import List, Tuple, Any

def data_handler(data: List[Any] | Tuple[Any]) -> str:
    output = ""
    
    for index in data:
        output += str(index)
        output += "$$"
        
    return output
    
def text_for_generate_avatar_handler(text: str) -> str:         
    listed_text = text.strip().split()
     
    if len(listed_text) > 1:
        return listed_text[0][0] + listed_text[-1][0]
    return listed_text[0][0]
    

if __name__ == "__main__":
    # print(data_handler([1314, "f3wggw", False]))
    print(text_for_generate_avatar_handler("test nickname"))
