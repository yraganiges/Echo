with open("server\\ai\\datasets\\danger_messages.txt", "r") as file:
    for index in file.read().split("$"):
        try:
            print(index[-1])
        except IndexError:
            pass
        