import json

with open("server\\data\\server_config.json") as file:
    server_conf = json.load(file)
    
with open("server\\data\\app_config.json") as file:
    app_conf = json.load(file)