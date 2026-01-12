import pytest
from pydantic import ValidationError
from backend.schemas import TodoCreate

def test_title_cannot_be_empty():
    with pytest.raises(ValidationError):
        TodoCreate(title="")

def test_title_with_only_spaces_is_invalid():
    with pytest.raises(ValidationError):
        TodoCreate(title="   ")

def test_valid_title_is_accepted():
    todo = TodoCreate(title="Buy milk")
    assert todo.title == "Buy milk"
