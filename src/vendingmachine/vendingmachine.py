from .lib import (
    check_coin, get_product_by_button, get_price_by_product, coin_sum,
    get_all_products, get_currency,
    get_acceptable_coins, add_coin_boxes, coin_by_descending_value,
    get_coin_value
)

INSERT_COIN = "INSERT COIN"
SOLD_OUT = "SOLD OUT"
EXACT_CHANGE_ONLY = "EXACT CHANGE ONLY"
THANK_YOU = "THANK YOU"
PRICE = "PRICE "


def as_currency(pennies: int, prefix: str = "", divisor: int = 100, decimals: int = 2) -> str:
    return f"{prefix}{get_currency()}{pennies / divisor:.{decimals}f}"


class VendingMachine:
    """Vending Machine Simulator"""
    SOLD_OUT = -1
    display: str

    def __init__(self) -> None:
        self.coin_buffer = dict.fromkeys(get_acceptable_coins(), 0)
        self.coin_box = dict.fromkeys(get_acceptable_coins(), 0)
        self.coin_return: list[str] = []
        self.hopper: list[str] = []
        self.selected_product = None
        self.current_amount = 0
        self.stock = {}
        self.reset_display()

    def reset_display(self) -> None:
        coin_box_has_every_coin = all((count for count in self.coin_box.values()))
        self.display = INSERT_COIN if coin_box_has_every_coin else EXACT_CHANGE_ONLY

    def insert_coin(self, coin: str) -> None:
        if value := check_coin(coin):
            self.coin_buffer[coin] += 1
            self.current_amount += value
            self._update_display()
        else:
            self.coin_return.append(coin)

    def select_product(self, button: str) -> str | None:
        self.selected_product = product = get_product_by_button(button)

        if self._is_sold_out(product):  # selected product not available: do not sell
            self._update_display(self.SOLD_OUT)
            self.selected_product = None
            return None

        price = get_price_by_product(self.selected_product)
        self._update_display(price)

        if self.current_amount < price:  # not enough coins: do not sell
            self.selected_product = None
            return product

        change = self._can_give_change(price)
        if change < 0:  # can not give change: do not sell, return coins
            self.selected_product = None
            self.return_coins()
            return product

        # dispense, if enough payment, selected product available and if change can be made
        self._dispense()
        self._collect_coins_from_buffer()
        self._make_change(change)

        return product

    def return_coins(self) -> None:
        self._return_coins_from_buffer()
        self.selected_product = None
        self.current_amount = 0
        self._update_display()

    def check_display(self) -> str:
        display = self.display
        self._update_display()
        return display

    def _dispense(self) -> None:
        self.hopper.append(self.selected_product)
        self.stock[self.selected_product] -= 1
        self.selected_product = None
        self.current_amount = 0
        self._update_display(self.current_amount)

    def _collect_coins_from_buffer(self) -> None:
        for coin in self.coin_buffer:
            self.coin_box[coin] += self.coin_buffer[coin]
            self.coin_buffer[coin] = 0

    def _can_give_change(self, price: int) -> int:
        all_coins = add_coin_boxes(self.coin_box, self.coin_buffer)
        change = coin_sum(self.coin_buffer) - price
        ordered_coins = coin_by_descending_value()
        amount = 0
        try:
            current_coin = next(ordered_coins)
            while amount <= change:
                value = get_coin_value(current_coin)
                while all_coins[current_coin] > 0 and amount + value <= change:
                    amount += value
                    all_coins[current_coin] -= 1
                current_coin = next(ordered_coins)
        except StopIteration:
            pass
        return change if amount == change else -1

    def _make_change(self, change: int) -> None:
        ordered_coins = coin_by_descending_value()
        coin = next(ordered_coins)
        value = get_coin_value(coin)
        coin_return = []
        while change > 0:
            if value <= change and self.coin_box[coin] > 0:
                coin_return.append(coin)
                self.coin_box[coin] -= 1
                change -= value
            else:
                coin = next(ordered_coins)
                value = get_coin_value(coin)
        self.coin_return.extend(coin_return)

    def _update_display(self, price: int | None = None):
        if price is not None and price < 0:
            self.display = SOLD_OUT
        elif price is not None and price == 0:
            self.display = THANK_YOU
        elif price is not None and price > 0:
            self.display = as_currency(price, prefix=PRICE)
        elif coin_sum(self.coin_buffer) > 0:
            self.display = as_currency(self.current_amount)
        elif any((count == 0 for count in self.coin_box.values())):
            self.display = EXACT_CHANGE_ONLY
        else:
            self.display = INSERT_COIN

    def _return_coins_from_buffer(self) -> None:
        for coin in self.coin_buffer:
            self.coin_return.extend([coin] * self.coin_buffer[coin])
            self.coin_buffer[coin] = 0

    def _is_sold_out(self, product: str) -> bool:
        return self.stock.get(product, 0) == 0


def restock_products(vending_machine: VendingMachine, *, items_per_stock: int = 10) -> None:
    for product in get_all_products():
        vending_machine.stock[product] = items_per_stock
    vending_machine.reset_display()


def refill_money_box(vending_machine: VendingMachine, *, items_per_coin: int = 10) -> None:
    for coin in get_acceptable_coins():
        vending_machine.coin_box[coin] = items_per_coin
    vending_machine.reset_display()
