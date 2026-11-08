import pytest
from unittest.mock import Mock

from burger import Burger
from bun import Bun
from ingredient import Ingredient

@pytest.fixture
def burger():
    # Создаём новый объект бургера перед каждым тестом.
    return Burger()


@pytest.fixture
def bun():
    # Создаём мок булочки вместо реального объекта.
    # Задаём значения, которые будут возвращать методы булочки.
    mock_bun = Mock(spec=Bun)
    mock_bun.get_name.return_value = "black bun"
    mock_bun.get_price.return_value = 100
    return mock_bun


@pytest.fixture
def sauce():
    # Создаём мок соуса с заданными типом, названием и ценой.
    mock_ingredient = Mock(spec=Ingredient)
    mock_ingredient.get_type.return_value = "SAUCE"
    mock_ingredient.get_name.return_value = "hot sauce"
    mock_ingredient.get_price.return_value = 100
    return mock_ingredient


@pytest.fixture
def filling():
    # Создаём мок начинки с заданными типом, названием и ценой.
    mock_ingredient = Mock(spec=Ingredient)
    mock_ingredient.get_type.return_value = "FILLING"
    mock_ingredient.get_name.return_value = "cutlet"
    mock_ingredient.get_price.return_value = 200
    return mock_ingredient