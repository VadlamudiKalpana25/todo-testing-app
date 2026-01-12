import pytest
from pydantic import ValidationError
from backend.schemas import TodoCreate

@pytest.mark.parametrize("length,should_fail", [
    (201, True),
    (200, False),
    (1,   False),
])
def test_title_length_rules(length, should_fail):
    title = "a" * length
    if should_fail:
        with pytest.raises(ValidationError):
            TodoCreate(title=title)
    else:
        todo = TodoCreate(title=title)
        assert todo.title == title
