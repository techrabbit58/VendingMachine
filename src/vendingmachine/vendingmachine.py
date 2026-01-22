from .lib import check_coin, get_product_by_button, get_price_by_product, coin_sum, fewest_coins_that_match_exact_amount


class VendingMachine:
    """Vending Machine Simulator"""

    def __init__(self) -> None:
        self.coin_buffer: list[str] = []
        self.coin_return: list[str] = []
        self.hopper: list[str] = []
        self.selected_product = None
        self.current_amount = 0
        self.display = "INSERT COIN"

    def insert_coin(self, coin: str) -> None:
        if value := check_coin(coin):
            self.coin_buffer.append(coin)
            self.current_amount += value
            self._update_display()
        else:
            self.coin_return.append(coin)

    def select_product(self, button: str) -> str:
        self.selected_product = product = get_product_by_button(button)
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
        if price == 0:
            self.display = "THANK YOU"
        elif price is not None and price > 0:
            self.display = f"PRICE ${price / 100:.2f}"
        elif len(self.coin_buffer) > 0:
            self.display = f"${self.current_amount / 100:.2f}"
        else:
            self.display = "INSERT COIN"

    def _dispense(self) -> None:
        self.hopper.append(self.selected_product)
        self.selected_product = None
        self.current_amount = 0
        self._update_display(0)

    def _make_change(self, price: int) -> None:
        change = coin_sum(self.coin_buffer) - price
        if change > 0:
            self.coin_return.extend(fewest_coins_that_match_exact_amount(change))

    def return_coins(self) -> None:
        ...
