import textwrap
import tkinter as tk
from functools import partial
from queue import Queue
from tkinter.ttk import Button, LabelFrame, Label

from .conf import BUTTONS, COINS
from .lib import get_product_by_button
from .vendingmachine import VendingMachine, restock_products, refill_money_box


class App(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        v = VendingMachine()
        restock_products(v)
        refill_money_box(v)
        self.vending_machine = v

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.minsize(400, 380)

        self.title("Vending Machine")

        self.job_id = Queue()

        self.button_area = LabelFrame(self, text="Products", borderwidth=5, labelanchor="n")
        self.button_area.grid(column=0, row=0, padx=(15, 5), pady=10, ipady=5, sticky="nwse")
        self.button_area.columnconfigure(0, weight=1)
        self.button_area.columnconfigure(1, weight=1)
        self.button_area.columnconfigure(2, weight=1)

        self.buttons = []
        for button in BUTTONS:
            product = get_product_by_button(button)
            b = Button(
                self.button_area,
                text=product.title(),
                command=partial(self.on_select_product, button)
            )
            b.grid(sticky="n", column=1)
            self.buttons.append(b)

        self.coin_area = LabelFrame(self, text="Coins", borderwidth=5, labelanchor="n")
        self.coin_area.grid(column=1, row=0, padx=(5, 15), pady=10, ipady=5, sticky="nwse")
        self.coin_area.columnconfigure(0, weight=1)
        self.coin_area.columnconfigure(1, weight=1)
        self.coin_area.columnconfigure(2, weight=1)

        self.coins = []
        for coin in COINS:
            c = Button(
                self.coin_area,
                text=coin.title(),
                command=partial(self.on_insert_coin, coin)
            )
            c.grid(sticky="n", column=1)
            self.coins.append(c)

        self.display_area = LabelFrame(self, text="Display", borderwidth=5, labelanchor="n")
        self.display_area.grid(
            column=0, row=1, columnspan=2, padx=15, pady=(0, 5), ipady=5, sticky="we")
        self.display_area.columnconfigure(0, weight=1)
        self.display_area.columnconfigure(1, weight=1)
        self.display_area.columnconfigure(2, weight=1)

        self.display = Label(self.display_area, text=self.vending_machine.check_display())
        self.display.grid(sticky="n", columnspan=3, column=0)

        self.coin_return_area = LabelFrame(self, text="Coin Return", borderwidth=5, labelanchor="n")
        self.coin_return_area.grid(
            column=0, row=2, columnspan=2, padx=15, pady=(0, 5), ipady=5, sticky="we")
        self.coin_return_area.columnconfigure(0, weight=1)
        self.coin_return_area.columnconfigure(1, weight=1)
        self.coin_return_area.columnconfigure(2, weight=1)

        self.coin_return_button = Button(
            self.coin_return_area,
            text="Return coins",
            command=self.on_return_coins
        )
        self.coin_return_button.grid(sticky="w", row=0, column=0)

        self.takeout_coins_button = Button(
            self.coin_return_area,
            text="Take out",
            command=self.on_takeout_coins
        )
        self.takeout_coins_button.grid(sticky="w", row=1, column=0)

        self.coin_return = Label(self.coin_return_area, text="Empty")
        self.coin_return.grid(sticky="w", row=0, column=1, columnspan=2)

        self.hopper_area = LabelFrame(self, text="Hopper", borderwidth=5, labelanchor="n")
        self.hopper_area.grid(
            column=0, row=3, columnspan=2, padx=15, pady=(0, 25), ipady=5, sticky="we")
        self.hopper_area.columnconfigure(0, weight=1)
        self.hopper_area.columnconfigure(1, weight=1)
        self.hopper_area.columnconfigure(2, weight=1)

        self.products = Label(self.hopper_area, text="Empty")
        self.products.grid(sticky="w", row=0, column=1, columnspan=2)

        self.takeout_products_button = Button(
            self.hopper_area,
            text="Take out",
            command=self.on_takeout_products
        )
        self.takeout_products_button.grid(sticky="w", row=0, column=0)

        self.resizable(False, False)

    def on_select_product(self, button: str) -> None:
        self.vending_machine.select_product(button)
        self._update_display()
        # noinspection PyTypeChecker
        self.job_id.put(self.after(2000, self._update_display))

    def on_insert_coin(self, coin: str) -> None:
        self.vending_machine.insert_coin(coin)
        self._update_display()

    def on_return_coins(self) -> None:
        self.vending_machine.return_coins()
        self._update_display()

    def on_takeout_coins(self) -> None:
        self.vending_machine.coin_return.clear()
        self._update_display()

    def on_takeout_products(self) -> None:
        self.vending_machine.hopper.clear()
        self._update_display()

    def _update_display(self) -> None:
        while self.job_id.qsize() > 0:
            self.after_cancel(self.job_id.get())
        self.coin_return["text"] = textwrap.shorten(
            " ".join(self.vending_machine.coin_return).upper(),
            40) or "Empty"
        self.products["text"] = textwrap.shorten(
            " ".join(self.vending_machine.hopper).upper(),
            40) or "Empty"
        self.display["text"] = self.vending_machine.check_display()

    def run(self) -> None:
        self.mainloop()


def main() -> None:
    app = App()
    app.run()


main()
