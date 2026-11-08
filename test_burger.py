
import pytest
from unittest.mock import Mock

from ingredient import Ingredient


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
            (0, ["cutlet", "sausage"]),
            (1, ["hot sauce", "sausage"]),
            (2, ["hot sauce", "cutlet"]),
        ],
    )
    def test_remove_ingredient(
        self, burger, sauce, filling, index, expected
    ):
        # Создаём третий ингредиент, чтобы проверить удаление
        # из разных позиций.
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

    def test_move_ingredient(self, burger, sauce, filling):
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
            ([], 200),               # Только две булочки.
            ([100], 300),            # Булочки и один ингредиент.
            ([100, 200], 500),       # Булочки и два ингредиента.
            ([100, 200, 300], 800),  # Булочки и три ингредиента.
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
        self, burger, bun, sauce, filling
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
