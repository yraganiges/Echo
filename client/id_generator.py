import random

def generate_user_id(length: int = 16) -> str:
        output: str = ""
        
        for _ in range(length):
            if random.choice(("num", "lett")) == "num":
                output += str(random.choice(list(range(0, 10))))
            else:
                output += random.choice("qwertyuiopasdfghjklzxcvbnm")
                
        return output