from .conf import COINS, VALUES, BUTTONS, PRODUCTS, PRICE_POINTS


def test_COINS_and_VALUES_must_be_same_length():
    assert len(COINS) == len(VALUES)


def test_BUTTONS_PRODUCTS_and_PRICE_POINTS_must_be_same_length():
    assert len(BUTTONS) == len(PRODUCTS) == len(PRICE_POINTS)
