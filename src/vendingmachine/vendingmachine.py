from .lib import (
    check_coin, get_product_by_button, get_price_by_product, coin_sum,
    fewest_coins_that_match_exact_amount, get_all_products, get_currency
)


class VendingMachine:
    """Vending Machine Simulator"""
    SOLD_OUT = -1

    def __init__(self) -> None:
        self.coin_buffer: list[str] = []
        self.coin_return: list[str] = []
        self.hopper: list[str] = []
        self.selected_product = None
        self.current_amount = 0
        self.display = "INSERT COIN"
        self.stock = {}

    def insert_coin(self, coin: str) -> None:
        if value := check_coin(coin):
            self.coin_buffer.append(coin)
            self.current_amount += value
            self._update_display()
        else:
            self.coin_return.append(coin)

    def select_product(self, button: str) -> str | None:
        self.selected_product = product = get_product_by_button(button)
        if self._is_sold_out(product):
            self._update_display(self.SOLD_OUT)
            self.selected_product = None
            return None
        price = get_price_by_product(self.selected_product)
        self._update_display(price)
        if self.current_amount < price:
            self.selected_product = None
        else:
            self._dispense()
            self._make_change(price)
            self.coin_buffer.clear()
        return product

    def check_display(self) -> str:
        display = self.display
        self._update_display()
        return display

    def _update_display(self, price: int | None = None):
        if price is not None and price < 0:
            self.display = "SOLD OUT"
        elif price is not None and price == 0:
            self.display = "THANK YOU"
        elif price is not None and price > 0:
            self.display = f"PRICE {get_currency()}{price / 100:.2f}"
        elif len(self.coin_buffer) > 0:
            self.display = f"{get_currency()}{self.current_amount / 100:.2f}"
        else:
            self.display = "INSERT COIN"

    def _dispense(self) -> None:
        self.hopper.append(self.selected_product)
        self.stock[self.selected_product] -= 1
        self.selected_product = None
        self.current_amount = 0
        self._update_display(self.current_amount)

    def _make_change(self, price: int) -> None:
        change = coin_sum(self.coin_buffer) - price
        if change > 0:
            self.coin_return.extend(fewest_coins_that_match_exact_amount(change))

    def return_coins(self) -> None:
        self.coin_return.extend(self.coin_buffer)
        self.coin_buffer.clear()
        self.selected_product = None
        self.current_amount = 0
        self._update_display()

    def _is_sold_out(self, product: str) -> bool:
        return self.stock.get(product, 0) == 0


def restock_all(vending_machine: VendingMachine, items_per_stock: int = 10) -> None:
    for product in get_all_products():
        vending_machine.stock[product] = items_per_stock
