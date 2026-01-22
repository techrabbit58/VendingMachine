from .lib import check_coin, FiFo, get_product_by_button, get_price_by_product


class VendingMachine:
    """Vending Machine Simulator"""

    def __init__(self) -> None:
        self.coin_buffer: FiFo[str] = FiFo("event queue")
        self.coin_return: FiFo[str] = FiFo("coin return")
        self.hopper: list[str] = []
        self.selected_product = None
        self.current_amount = 0
        self.display = "INSERT COIN"

    def insert_coin(self, coin: str) -> None:
        if value := check_coin(coin):
            self.coin_buffer.put(coin)
            self.current_amount += value
            self._update_display()
        else:
            self.coin_return.put(coin)

    def select_product(self, button: str) -> str:
        self.selected_product = product = get_product_by_button(button)
        price = get_price_by_product(self.selected_product)
        self._update_display(price)
        if self.current_amount < price:
            self.selected_product = None
        else:
            self._dispense()
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
        elif self.coin_buffer.qsize() > 0:
            self.display = f"${self.current_amount / 100:.2f}"
        else:
            self.display = "INSERT COIN"

    def _dispense(self) -> None:
        self.hopper.append(self.selected_product)
        self.selected_product = None
        self.current_amount = 0
        while self.coin_buffer.qsize() > 0:
            self.coin_buffer.get()
        self._update_display(0)
