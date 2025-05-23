"""
conftest.py for pytest configuration.
"""

import pytest

@pytest.fixture
def my_data():
    return "Hello, differently!"