from unittest.mock import patch

from tools import extract_action_items_rule_based, extract_action_items_llm


def test_rule_based_extraction():
    notes = """
    Meeting notes:
    TODO: fix login bug
    - update README
    Maybe we should improve the UI later
    write tests for auth
    """

    items = extract_action_items_rule_based(notes)

    assert "fix login bug" in items
    assert "update README" in items
    assert "write tests for auth" in items


def test_llm_extraction_real():
    notes = """
    Meeting notes:
    Tomorrow we need to fix the login bug.
    Also update the README.
    Maybe we should improve the UI later.
    Write tests for auth.
    """

    items = extract_action_items_llm(notes)

    assert len(items) >= 2
    joined = " ".join(items).lower()

    assert "fix" in joined
    assert "readme" in joined


@patch("tools.ask_llm")
def test_llm_extraction_with_mock(mock_ask_llm):
    mock_ask_llm.return_value = (
        '{"action_items": ["Fix login bug", "Update README", "Write auth tests"]}'
    )

    notes = """
    Tomorrow we need to fix the login bug.
    Also update the README.
    Write tests for auth.
    """

    items = extract_action_items_llm(notes)

    assert items == ["Fix login bug", "Update README", "Write auth tests"]


@patch("tools.ask_llm")
def test_llm_extraction_with_invalid_json(mock_ask_llm):
    mock_ask_llm.return_value = "not a valid json response"

    notes = "Please fix the login bug."

    items = extract_action_items_llm(notes)

    assert items == []