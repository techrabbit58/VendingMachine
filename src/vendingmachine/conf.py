import json
from pathlib import Path

configuration = json.load(Path(__file__).with_suffix(".json").open())

COINS = tuple(coin["name"] for coin in configuration["coins"])
VALUES = tuple(coin["value"] for coin in configuration["coins"])

PRODUCTS = tuple(product["name"] for product in configuration["products"])
PRICES = tuple(product["price"] for product in configuration["products"])
BUTTONS = tuple(product["button"] for product in configuration["products"])

CURRENCY = configuration["strings"].get("currency", "$")

INSERT_COIN = configuration["strings"].get("insert coin", "INSERT COIN")
SOLD_OUT = configuration["strings"].get("sold out", "SOLD OUT")
EXACT_CHANGE_ONLY = configuration["strings"].get("exact change only", "EXACT CHANGE ONLY")
THANK_YOU = configuration["strings"].get("thank you", "THANK YOU")
PRICE = configuration["strings"].get("price", "PRICE ")
