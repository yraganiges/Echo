from typing import List, Tuple, Any

def data_handler(data: List[Any] | Tuple[Any]) -> str:
    output = ""
    
    for index in data:
        output += str(index)
        output += "$$"
        
    return output

if __name__ == "__main__":
    print(data_handler([1314, "f3wggw", False]))