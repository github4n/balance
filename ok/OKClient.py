import sys
import importlib

sys.path.append("/home/balance")
importlib.reload(sys)
import tokens.Token as Token
import api.OkexClientV3 as Client
import configparser
import json
import threading

# read config
config = configparser.ConfigParser()
config.read("config.ini")

if __name__ == '__main__':
    symbols = json.loads(config.get("trade", "symbol"))
    if len(symbols) > 1:
        for symbol in symbols:
            threading.Thread(target=Token.__main__, args=(Client.OkexClient(), symbol,)).start()
    else:
        Token.__main__(Client.OkexClient(), symbols[0])
