from .conf import COINS


def test_return_coins_on_return_button_pressed(vending_machine):
    v = vending_machine
    coins = list(COINS)
    for coin in coins:
        v.insert_coin(coin)
    assert v.coin_buffer == coins, "coins in buffer (before)"
    v.return_coins()
    assert v.coin_buffer == [], "coins in buffer (after)"
    assert v.coin_return == coins, "coins in coin return (final)"
    assert v.selected_product is None
    assert v.current_amount == 0
    assert v.check_display() == "INSERT COIN"
