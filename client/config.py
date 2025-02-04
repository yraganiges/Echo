import json

with open("client\\data\\ui_config.json") as file:
    ui_config = json.load(file)
    
with open("client\\data\\app_config.json") as file:
    app_config = json.load(file)
    
with open("client\\data\\paths.json") as file:
    paths_config = json.load(file)
