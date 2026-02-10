from .conf import COINS, INSERT_COIN


def test_return_coins_on_return_button_pressed(vending_machine):
    v = vending_machine
    inserted_coins = dict.fromkeys(COINS, 2)
    returned_coins = []
    for coin in inserted_coins:
        for _ in range(inserted_coins[coin]):
            v.insert_coin(coin)
            returned_coins.append(coin)
    assert v.coin_buffer == inserted_coins, "coins in buffer (before)"
    v.return_coins()
    assert v.coin_buffer == dict.fromkeys(COINS, 0), "coins in buffer (after)"
    assert v.coin_return == returned_coins, "coins in coin return (final)"
    assert v.selected_product is None
    assert v.current_amount == 0
    assert v.check_display() == INSERT_COIN
