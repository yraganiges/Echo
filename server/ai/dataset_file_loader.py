def proccesing_data(file_path: str) -> None:
    try:
        chars ='#$%&()*+-./:;<=>?@[]^_{|}~`'
        output = ""
        
        with open(file_path, "r") as file:
            for index in file.read().strip().lower():
                if index not in chars:
                    output += index
            
        with open(file_path, "w") as file:
            file.write(output)
    except:
        raise ValueError("failed to write proccesing data to file!")             
        
        
if __name__ == "__main__":
    proccesing_data(file_path = "server\\ai\\datasets\\danger_messages.csv")