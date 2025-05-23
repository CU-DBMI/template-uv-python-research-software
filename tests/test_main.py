"""
Tests for the main module.
"""

from example_project.main import show_message


def test_show_message() -> None:
    """
    Test the show_message function.
    """

    # Test default message
    result = show_message()
    assert result.shape == (1, 1)
    assert result.iloc[0, 0] == "Hello, world!"

    # Test custom message
    custom_message = "Custom message"
    result = show_message(custom_message)
    assert result.shape == (1, 1)
    assert result.iloc[0, 0] == custom_message
