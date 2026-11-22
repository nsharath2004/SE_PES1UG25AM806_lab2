
import pytest

from credit_card_rewards import (
    reward_points,
    late_payment_fee,
    card_status
)


# REWARD POINTS - BRANCH TESTS

def test_unknown_card():
    with pytest.raises(ValueError):
        reward_points("silver", 1000, "grocery", False)


def test_valid_classic_card():
    assert reward_points("classic", 1000, "grocery", False) == 10


def test_invalid_zero_amount():
    with pytest.raises(ValueError):
        reward_points("gold", 0, "grocery", False)


def test_invalid_negative_amount():
    with pytest.raises(ValueError):
        reward_points("gold", -100, "grocery", False)


def test_fuel_category():
    assert reward_points("gold", 1000, "fuel", False) == 0


def test_grocery_category():
    assert reward_points("gold", 1000, "grocery", False) == 20


def test_dining_category():
    assert reward_points("gold", 1000, "dining", False) == 40


def test_travel_category():
    assert reward_points("platinum", 1000, "travel", False) == 80


def test_weekend_non_classic():
    assert reward_points("gold", 1000, "grocery", True) == 70


def test_weekend_classic():
    assert reward_points("classic", 1000, "grocery", True) == 10


def test_weekday_non_classic():
    assert reward_points("platinum", 1000, "grocery", False) == 40


# LATE PAYMENT FEE - BRANCH TESTS

def test_no_days_late():
    assert late_payment_fee(5000, 0) == 0


def test_negative_days_late():
    assert late_payment_fee(5000, -1) == 0


def test_zero_outstanding():
    assert late_payment_fee(0, 10) == 0


def test_negative_outstanding():
    assert late_payment_fee(-100, 10) == 0


def test_outstanding_1000():
    assert late_payment_fee(1000, 10) == 100


def test_outstanding_1001():
    assert late_payment_fee(1001, 10) == 500


def test_outstanding_10000():
    assert late_payment_fee(10000, 10) == 500


def test_outstanding_above_10000():
    assert late_payment_fee(10001, 10) == 1000


def test_exactly_30_days_late():
    assert late_payment_fee(5000, 30) == 500


def test_more_than_30_days_late():
    assert late_payment_fee(5000, 31) == 1250


# CARD STATUS - BRANCH TESTS

def test_frozen_card():
    assert card_status(95, 3, True) == "frozen"


def test_blocked_card():
    assert card_status(50, 3, False) == "blocked"


def test_not_blocked():
    assert card_status(50, 2, False) == "watch"


def test_over_limit():
    assert card_status(91, 0, False) == "over limit risk"


def test_not_over_limit():
    assert card_status(90, 0, False) == "watch"


def test_watch_due_to_utilisation():
    assert card_status(31, 0, False) == "watch"


def test_watch_due_to_missed_payment():
    assert card_status(20, 1, False) == "watch"


def test_good_status():
    assert card_status(30, 0, False) == "good"
