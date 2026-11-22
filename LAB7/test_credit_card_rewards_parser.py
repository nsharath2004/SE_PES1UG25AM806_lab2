
from hypothesis import given, strategies as st

from credit_card_rewards_parser import (
    mask_card_number,
    parse_transaction,
    parse_statement_total
)


@given(st.text() | st.none())
def test_mask_card_number_no_crash(s):
    try:
        mask_card_number(s)
    except Exception as e:
        assert False, f"mask_card_number crashed with input {s!r}: {e}"


@given(st.text() | st.none())
def test_parse_transaction_no_crash(s):
    try:
        parse_transaction(s)
    except Exception as e:
        assert False, f"parse_transaction crashed with input {s!r}: {e}"


@given(st.text() | st.none())
def test_parse_statement_total_no_crash(s):
    try:
        parse_statement_total(s)
    except Exception as e:
        assert False, f"parse_statement_total crashed with input {s!r}: {e}"
