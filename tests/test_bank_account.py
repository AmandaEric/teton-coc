# tests/test_bank_account.py
import pytest
from bank_account import (
    create_account,
    deposit,
    withdraw,
    transfer,
    account_str,
)

def test_create_account_default_balance():
    acct = create_account("Alice")
    assert acct["name"] == "Alice"
    assert acct["balance"] == 0
    assert acct["transactions"] == []

def test_create_account_with_opening_balance():
    acct = create_account("Bob", opening_balance=100)
    assert acct["balance"] == 100
    assert acct["transactions"] == [("opening_balance", 100)]

def test_deposit_positive_amount():
    acct = create_account("Carol")
    deposit(acct, 50)
    assert acct["balance"] == 50
    assert acct["transactions"][-1] == ("deposit", 50)

def test_deposit_negative_raises():
    acct = create_account("Dan")
    with pytest.raises(ValueError):
        deposit(acct, -10)

def test_withdraw_success():
    acct = create_account("Eve", opening_balance=100)
    withdraw(acct, 40)
    assert acct["balance"] == 60
    assert acct["transactions"][-1] == ("withdraw", 40)

def test_withdraw_insufficient_raises():
    acct = create_account("Frank", opening_balance=20)
    with pytest.raises(ValueError):
        withdraw(acct, 30)

def test_transfer_between_accounts():
    a = create_account("Gina", opening_balance=200)
    b = create_account("Hank", opening_balance=50)
    result = transfer(a, b, 75)
    assert result is True
    assert a["balance"] == 125
    assert b["balance"] == 125
    assert a["transactions"][-1] == ("transfer_out", 75)
    assert b["transactions"][-1] == ("transfer_in", 75)

def test_transfer_insufficient_raises():
    a = create_account("Ivy", opening_balance=10)
    b = create_account("Jack", opening_balance=0)
    with pytest.raises(ValueError):
        transfer(a, b, 20)

def test_transfer_invalid_account_raises():
    a = create_account("Kara", opening_balance=100)
    with pytest.raises(ValueError):
        transfer(a, "not_an_account", 10)

def test_str_like_output():
    acct = create_account("Leo", opening_balance=30)
    s = account_str(acct)
    assert "Leo" in s
    assert "30" in s