from vendingmachine.conf import VALUES
from vendingmachine.lib import get_coin_name_by_value


def overpaid(price: int) -> dict[str, int]:
    coin, value = max_coin()
    coin_box = {coin: 0}
    amount = 0
    while amount <= price:
        coin_box[coin] += 1
        amount += value
    return coin_box


def min_coin() -> tuple[str, int]:
    value = min(VALUES)
    return get_coin_name_by_value(value), value


def max_coin() -> tuple[str, int]:
    value = max(VALUES)
    return get_coin_name_by_value(value), value
