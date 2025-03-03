
def is_remind_message(message: str) -> bool:
    spec_words = ("упом напом завтра вчера вечер утр врем важн сроч забу забы вспом числ дат скор сентяб октяб нояб декабр январ феврал март апрел май мае мая июн июл август встреч мероприят ")
    
    for word in message.split():
        for index in spec_words.split():
            if word.lower().count(index) > 0:
                return True
        
    return False

if __name__ == "__main__":
    print(is_remind_message("встреча с  клиентом 10 октября в 14:00"))