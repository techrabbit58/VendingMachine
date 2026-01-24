import json
from pathlib import Path

configuration = json.load(Path(__file__).with_suffix(".json").open())

COINS = tuple(coin["name"] for coin in configuration["coins"])
VALUES = tuple(coin["value"] for coin in configuration["coins"])

PRODUCTS = tuple(product["name"] for product in configuration["products"])
PRICES = tuple(product["price"] for product in configuration["products"])
BUTTONS = tuple(product["button"] for product in configuration["products"])

CURRENCY = configuration["currency"]
