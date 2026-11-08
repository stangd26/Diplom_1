import pytest
from unittest.mock import Mock

from burger import Burger
from bun import Bun
from ingredient import Ingredient

from test_data import (
    BUN_NAME,
    BUN_PRICE,
    SAUCE_NAME,
    SAUCE_PRICE,
    SAUCE_TYPE,
    FILLING_NAME,
    FILLING_PRICE,
    FILLING_TYPE,
)

@pytest.fixture
def burger():
    # Создаём новый объект бургера перед каждым тестом.
    return Burger()


@pytest.fixture
def bun():
    # Создаём мок булочки вместо реального объекта.
    # Задаём значения, которые будут возвращать методы булочки.
    mock_bun = Mock(spec=Bun)
    mock_bun.get_name.return_value = BUN_NAME
    mock_bun.get_price.return_value = BUN_PRICE
    return mock_bun


@pytest.fixture
def sauce():
    # Создаём мок соуса с заданными типом, названием и ценой.
    mock_ingredient = Mock(spec=Ingredient)
    mock_ingredient.get_name.return_value = SAUCE_NAME
    mock_ingredient.get_price.return_value = SAUCE_PRICE
    mock_ingredient.get_type.return_value = SAUCE_TYPE
    return mock_ingredient


@pytest.fixture
def filling():
    # Создаём мок начинки с заданными типом, названием и ценой.
    mock_ingredient = Mock(spec=Ingredient)
    mock_ingredient.get_name.return_value = FILLING_NAME
    mock_ingredient.get_price.return_value = FILLING_PRICE
    mock_ingredient.get_type.return_value = FILLING_TYPE
    return mock_ingredient