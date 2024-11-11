from typing import Any, List
import validators

class link(object):
    def __init__(self, link: str) -> None:
        self.link = link
        
    def is_valid_url(self) -> bool:
        return validators.url(self.link)

class Message(object):
    def __init__(self, message: str) -> None:
        self.message = message
        
    def processing_message(self) -> List[Any]:
        output: List[Any] = []
        for index in self.message:
            if validators.url(index): #проверяем на ссылку
                output.append(("link", index))
            else:
                output.append(("text", index))
                
            #TODO Сделать пинг пользователя