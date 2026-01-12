import pytest
from pydantic import ValidationError
from backend.schemas import RegisterRequest  # change if your register schema name differs

def test_password_too_short_should_fail():
    with pytest.raises(ValidationError):
        RegisterRequest(email="tdd@test.com", password="Ab1")

def test_password_without_uppercase_should_fail():
    with pytest.raises(ValidationError):
        RegisterRequest(email="tdd@test.com", password="password1")

def test_password_without_digit_should_fail():
    with pytest.raises(ValidationError):
        RegisterRequest(email="tdd@test.com", password="Password")

def test_valid_password_should_pass():
    user = RegisterRequest(email="tdd@test.com", password="Password1")
    assert user.password == "Password1"
