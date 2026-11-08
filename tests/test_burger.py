import pytest
from unittest.mock import Mock

from burgers.ingredient import Ingredient

from test_data import (
    EXPECTED_RECEIPT_WITHOUT_INGREDIENTS,
    EXPECTED_RECEIPT_WITH_SAUCE_AND_FILLING,
    SAUCE_NAME,
    FILLING_NAME,
    SAUSAGE_NAME,
    EXPECTED_BURGER_PRICE_WITHOUT_INGREDIENTS,
    EXPECTED_BURGER_PRICE_WITH_ONE_INGREDIENT,
    EXPECTED_BURGER_PRICE_WITH_SAUCE_AND_FILLING,
    EXPECTED_BURGER_PRICE_WITH_THREE_INGREDIENTS,
    FIRST_INGREDIENT,
    SECOND_INGREDIENT,
    THIRD_INGREDIENT
)

class TestBurger:

    def test_burger_init(self, burger):
        # Проверяем, что при создании бургера булочка не установлена,
        # а список ингредиентов пуст.
        assert burger.bun is None
        assert burger.ingredients == []

    def test_set_buns(self, burger, bun):
        # Устанавливаем булочку и проверяем, что она сохранилась.
        burger.set_buns(bun)

        assert burger.bun is bun

    def test_add_ingredient(self, burger, sauce):
        # Добавляем ингредиент и проверяем, что он появился в списке.
        burger.add_ingredient(sauce)

        assert burger.ingredients == [sauce]

    @pytest.mark.parametrize(
        # Проверяем удаление ингредиента из разных позиций списка.
        # Для каждого индекса задаём ожидаемый порядок оставшихся ингредиентов.
        "index, expected",
        [
            (0, [FILLING_NAME, SAUSAGE_NAME]),
            (1, [SAUCE_NAME, SAUSAGE_NAME]),
            (2, [SAUCE_NAME, FILLING_NAME]),
        ],
    )
    def test_remove_ingredient(
        self, burger, sauce, filling, index, expected
    ):
        # Создаём третий ингредиент, чтобы проверить удаление
        # из разных позиций.
        sausage = Mock(spec=Ingredient)
        sausage.get_name.return_value = SAUSAGE_NAME

        # Подготавливаем список из трёх ингредиентов.
        burger.ingredients = [sauce, filling, sausage]

        # Удаляем ингредиент по индексу из параметров теста.
        burger.remove_ingredient(index)

        # Проверяем, что остались правильные ингредиенты
        # в правильном порядке.
        assert [
            ingredient.get_name() for ingredient in burger.ingredients
        ] == expected

    def test_move_ingredient(self, burger, sauce, filling):
        # Подготавливаем список ингредиентов.
        sausage = Mock(spec=Ingredient)
        sausage.get_name.return_value = SAUSAGE_NAME
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
            ([], EXPECTED_BURGER_PRICE_WITHOUT_INGREDIENTS),               # Только две булочки.
            ([FIRST_INGREDIENT], EXPECTED_BURGER_PRICE_WITH_ONE_INGREDIENT),            # Булочки и один ингредиент.
            ([FIRST_INGREDIENT, SECOND_INGREDIENT], EXPECTED_BURGER_PRICE_WITH_SAUCE_AND_FILLING),       # Булочки и два ингредиента.
            ([FIRST_INGREDIENT, SECOND_INGREDIENT, THIRD_INGREDIENT], EXPECTED_BURGER_PRICE_WITH_THREE_INGREDIENTS),  # Булочки и три ингредиента.
        ],
    )
    def test_get_price(
        self, burger, bun, ingredient_prices, expected_price
    ):
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

    def test_get_receipt_without_ingredients(self, burger, bun):
        # Проверяем формирование чека для бургера без ингредиентов.
        burger.set_buns(bun)

        assert burger.get_receipt() == EXPECTED_RECEIPT_WITHOUT_INGREDIENTS

    def test_get_receipt_with_sauce_and_filling(
        self, burger, bun, sauce, filling
    ):
        # Проверяем чек для бургера с соусом и начинкой.
        burger.set_buns(bun)
        burger.add_ingredient(sauce)
        burger.add_ingredient(filling)

        assert (
            burger.get_receipt()
            == EXPECTED_RECEIPT_WITH_SAUCE_AND_FILLING
        )
