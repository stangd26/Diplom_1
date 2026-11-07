import pytest
from unittest.mock import Mock

from bun import Bun
from ingredient import Ingredient
from burger import Burger


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


def test_burger_init(burger):
    # Проверяем, что при создании бургера булочка не установлена,
    # а список ингредиентов пуст.
    assert burger.bun is None
    assert burger.ingredients == []


def test_set_buns(burger, bun):
    # Устанавливаем булочку и проверяем, что она сохранилась.
    burger.set_buns(bun)

    assert burger.bun is bun


def test_add_ingredient(burger, sauce):
    # Добавляем ингредиент и проверяем, что он появился в списке.
    burger.add_ingredient(sauce)

    assert burger.ingredients == [sauce]


@pytest.mark.parametrize(
    # Проверяем удаление ингредиента из разных позиций списка.
    # Для каждого индекса задаём ожидаемый порядок оставшихся ингредиентов.
    "index, expected",
    [
        (0, ["cutlet", "sausage"]),
        (1, ["hot sauce", "sausage"]),
        (2, ["hot sauce", "cutlet"]),
    ],
)
def test_remove_ingredient(burger, sauce, filling, index, expected):
    # Создаём третий ингредиент, чтобы проверить удаление из разных позиций.
    sausage = Mock(spec=Ingredient)
    sausage.get_name.return_value = "sausage"

    # Подготавливаем список из трёх ингредиентов.
    burger.ingredients = [sauce, filling, sausage]

    # Удаляем ингредиент по индексу из параметров теста.
    burger.remove_ingredient(index)

    # Проверяем, что остались правильные ингредиенты
    # в правильном порядке.
    assert [
        ingredient.get_name() for ingredient in burger.ingredients
    ] == expected


def test_move_ingredient(burger, sauce, filling):
    # Подготавливаем список ингредиентов.
    sausage = Mock(spec=Ingredient)
    sausage.get_name.return_value = "sausage"
    burger.ingredients = [sauce, filling, sausage]

    # Перемещаем соус с позиции 0 на позицию 2.
    burger.move_ingredient(0, 2)

    # Проверяем новый порядок ингредиентов.
    assert burger.ingredients == [filling, sausage, sauce]


@pytest.mark.parametrize(
    # Проверяем расчёт стоимости для разного количества ингредиентов.
    # Цена булочки всегда 100, а булочек в бургере две.
    "ingredient_prices, expected_price",
    [
        ([], 200),                  # Только две булочки.
        ([100], 300),               # Булочки и один ингредиент.
        ([100, 200], 500),          # Булочки и два ингредиента.
        ([100, 200, 300], 800),     # Булочки и три ингредиента.
    ],
)
def test_get_price(burger, bun, ingredient_prices, expected_price):
    # Устанавливаем булочку.
    burger.set_buns(bun)

    # Создаём ингредиенты с ценами из параметров теста.
    # Моки позволяют проверять расчёт независимо от других классов.
    burger.ingredients = []

    for price in ingredient_prices:
        ingredient = Mock(spec=Ingredient)
        ingredient.get_price.return_value = price
        burger.add_ingredient(ingredient)

    # Проверяем итоговую стоимость бургера.
    assert burger.get_price() == expected_price

    # Проверяем, что цена булочки запрашивалась один раз.
    # Умножение на два выполняется уже внутри метода get_price().
    bun.get_price.assert_called_once_with()


def test_get_receipt_without_ingredients(burger, bun):
    # Проверяем формирование чека для бургера без ингредиентов.
    burger.set_buns(bun)

    # Задаём ожидаемый текст чека целиком,
    # включая переносы строк и стоимость.
    expected_receipt = (
        "(==== black bun ====)\n"
        "(==== black bun ====)\n"
        "\n"
        "Price: 200"
    )

    assert burger.get_receipt() == expected_receipt


def test_get_receipt_with_sauce_and_filling(
    burger, bun, sauce, filling
):
    # Проверяем чек для бургера с соусом и начинкой.
    burger.set_buns(bun)
    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)

    # Проверяем форматирование типов в нижнем регистре,
    # названия ингредиентов, их порядок и итоговую цену.
    expected_receipt = (
        "(==== black bun ====)\n"
        "= sauce hot sauce =\n"
        "= filling cutlet =\n"
        "(==== black bun ====)\n"
        "\n"
        "Price: 500"
    )

    assert burger.get_receipt() == expected_receipt
