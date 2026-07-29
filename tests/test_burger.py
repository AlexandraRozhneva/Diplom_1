import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


class TestBurger:
    """Тесты для класса Burger"""

    def test_burger_initialization(self, burger):
        """Тест инициализации бургера"""
        assert burger.bun is None
        assert len(burger.ingredients) == 0
        assert isinstance(burger.ingredients, list)

    @pytest.mark.parametrize("bun_name, bun_price", [
        ("black bun", 100),
        ("white bun", 200),
        ("red bun", 300),
    ])
    def test_set_buns_with_real_bun(self, burger, bun_name, bun_price):
        """Тест установки булочки с реальными данными"""
        from praktikum.bun import Bun
        bun = Bun(bun_name, bun_price)
        burger.set_buns(bun)
        
        assert burger.bun == bun
        assert burger.bun.get_name() == bun_name
        assert burger.bun.get_price() == bun_price

    def test_set_buns_with_mock(self, burger, mock_bun):
        """Тест установки булочки с использованием мока"""
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun
        mock_bun.get_name.assert_called_once()
        mock_bun.get_price.assert_not_called()

    @pytest.mark.parametrize("ingredient_type, ingredient_name, ingredient_price", [
        ("SAUCE", "hot sauce", 100),
        ("FILLING", "cutlet", 150),
        ("SAUCE", "chili sauce", 200),
    ])
    def test_add_ingredient_with_real_ingredient(self, burger, ingredient_type, ingredient_name, ingredient_price):
        """Тест добавления ингредиента с реальными данными"""
        from praktikum.ingredient import Ingredient
        ingredient = Ingredient(ingredient_type, ingredient_name, ingredient_price)
        burger.add_ingredient(ingredient)
        
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient
        assert burger.ingredients[0].get_type() == ingredient_type
        assert burger.ingredients[0].get_name() == ingredient_name
        assert burger.ingredients[0].get_price() == ingredient_price

    def test_add_ingredient_with_mock(self, burger, mock_ingredient_sauce):
        """Тест добавления ингредиента с использованием мока"""
        burger.add_ingredient(mock_ingredient_sauce)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient_sauce

    @pytest.mark.parametrize("num_ingredients", [1, 3, 5])
    def test_add_multiple_ingredients(self, burger, mock_ingredient_sauce, num_ingredients):
        """Тест добавления нескольких ингредиентов"""
        for _ in range(num_ingredients):
            burger.add_ingredient(mock_ingredient_sauce)
        
        assert len(burger.ingredients) == num_ingredients
        assert all(ing == mock_ingredient_sauce for ing in burger.ingredients)

    @pytest.mark.parametrize("remove_index, expected_length", [
        (0, 2),
        (1, 2),
        (2, 2),
    ])
    def test_remove_ingredient(self, burger, mock_ingredient_sauce, mock_ingredient_filling, 
                               mock_ingredient_extra, remove_index, expected_length):
        """Тест удаления ингредиента по индексу"""
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        burger.add_ingredient(mock_ingredient_extra)
        
        burger.remove_ingredient(remove_index)
        assert len(burger.ingredients) == expected_length

    def test_remove_ingredient_first(self, burger, mock_ingredient_sauce, mock_ingredient_filling):
        """Тест удаления первого ингредиента"""
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient_filling

    def test_remove_ingredient_last(self, burger, mock_ingredient_sauce, mock_ingredient_filling):
        """Тест удаления последнего ингредиента"""
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        
        burger.remove_ingredient(1)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient_sauce

    @pytest.mark.parametrize("from_index, to_index, expected_order", [
        (0, 1, [1, 0]),
        (1, 0, [1, 0]),
        (0, 2, [1, 2, 0]),
        (2, 0, [2, 0, 1]),
    ])
    def test_move_ingredient(self, burger, mock_ingredient_sauce, mock_ingredient_filling,
                             mock_ingredient_extra, from_index, to_index, expected_order):
        """Тест перемещения ингредиента с различными параметрами"""
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        burger.add_ingredient(mock_ingredient_extra)
        
        original_ingredients = burger.ingredients.copy()
        burger.move_ingredient(from_index, to_index)
        
        # Проверяем порядок
        for i, idx in enumerate(expected_order):
            assert burger.ingredients[i] == original_ingredients[idx]

    def test_move_ingredient_same_position(self, burger, mock_ingredient_sauce, mock_ingredient_filling):
        """Тест перемещения ингредиента на ту же позицию"""
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        
        burger.move_ingredient(0, 0)
        assert burger.ingredients[0] == mock_ingredient_sauce
        assert burger.ingredients[1] == mock_ingredient_filling

    def test_get_price_without_bun(self, burger, mock_ingredient_sauce):
        """Тест получения цены без булочки - должно вызвать ошибку"""
        burger.add_ingredient(mock_ingredient_sauce)
        with pytest.raises(AttributeError):
            burger.get_price()

    @pytest.mark.parametrize("bun_price, expected_price", [
        (100, 200),
        (150, 300),
        (200, 400),
    ])
    def test_get_price_with_bun_only(self, burger, bun_price, expected_price):
        """Тест получения цены только с булочкой"""
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        assert burger.get_price() == expected_price
        mock_bun.get_price.assert_called_once()

    @pytest.mark.parametrize("bun_price, sauce_price, filling_price, expected_price", [
        (100, 50, 75, 325),
        (150, 30, 40, 370),
        (200, 100, 150, 650),
    ])
    def test_get_price_with_ingredients(self, burger, bun_price, sauce_price, filling_price, expected_price):
        """Тест получения цены с булочкой и ингредиентами"""
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        
        mock_sauce = Mock()
        mock_sauce.get_price.return_value = sauce_price
        
        mock_filling = Mock()
        mock_filling.get_price.return_value = filling_price
        
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        
        assert burger.get_price() == expected_price
        
        # Проверяем вызовы методов
        assert mock_bun.get_price.call_count == 1
        assert mock_sauce.get_price.call_count == 1
        assert mock_filling.get_price.call_count == 1

    def test_get_price_multiple_ingredients(self, burger, mock_bun):
        """Тест получения цены с несколькими ингредиентами"""
        burger.set_buns(mock_bun)
        
        mock_ingredients = []
        total_price = 0
        
        for price in [10, 20, 30, 40, 50]:
            mock_ing = Mock()
            mock_ing.get_price.return_value = price
            mock_ingredients.append(mock_ing)
            burger.add_ingredient(mock_ing)
            total_price += price
        
        expected_price = mock_bun.get_price() * 2 + total_price
        assert burger.get_price() == expected_price

    def test_get_receipt_without_bun(self, burger, mock_ingredient_sauce):
        """Тест получения чека без булочки - должно вызвать ошибку"""
        burger.add_ingredient(mock_ingredient_sauce)
        with pytest.raises(AttributeError):
            burger.get_receipt()

    @pytest.mark.parametrize("bun_name", [
        "black bun",
        "white bun",
        "red bun",
    ])
    def test_get_receipt_with_bun_only(self, burger, bun_name):
        """Тест получения чека только с булочкой"""
        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = 100
        
        burger.set_buns(mock_bun)
        
        expected_receipt = f"""(==== {bun_name} ====)
(==== {bun_name} ====)
Price: 200.0"""
        
        assert burger.get_receipt() == expected_receipt
        assert mock_bun.get_name.call_count == 2

    @pytest.mark.parametrize("ingredient_type, ingredient_name", [
        ("SAUCE", "hot sauce"),
        ("FILLING", "cutlet"),
        ("SAUCE", "chili sauce"),
    ])
    def test_get_receipt_with_one_ingredient(self, burger, mock_bun, ingredient_type, ingredient_name):
        """Тест получения чека с одним ингредиентом"""
        mock_bun.get_name.return_value = "test bun"
        burger.set_buns(mock_bun)
        
        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = ingredient_type
        mock_ingredient.get_name.return_value = ingredient_name
        mock_ingredient.get_price.return_value = 50
        
        burger.add_ingredient(mock_ingredient)
        
        expected_receipt = f"""(==== test bun ====)
= {ingredient_type.lower()} {ingredient_name} =
(==== test bun ====)
Price: 250.0"""
        
        assert burger.get_receipt() == expected_receipt

    def test_get_receipt_with_multiple_ingredients(self, burger, mock_bun):
        """Тест получения чека с несколькими ингредиентами"""
        mock_bun.get_name.return_value = "test bun"
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)
        
        ingredients_data = [
            ("SAUCE", "sauce1", 50),
            ("FILLING", "filling1", 75),
            ("SAUCE", "sauce2", 30),
            ("FILLING", "filling2", 40),
        ]
        
        for ing_type, ing_name, price in ingredients_data:
            mock_ing = Mock()
            mock_ing.get_type.return_value = ing_type
            mock_ing.get_name.return_value = ing_name
            mock_ing.get_price.return_value = price
            burger.add_ingredient(mock_ing)
        
        expected_lines = ["(==== test bun ====)"]
        for ing_type, ing_name, _ in ingredients_data:
            expected_lines.append(f"= {ing_type.lower()} {ing_name} =")
        expected_lines.append("(==== test bun ====)")
        expected_lines.append("Price: 395.0")
        
        expected_receipt = "\n".join(expected_lines)
        assert burger.get_receipt() == expected_receipt

    def test_get_receipt_with_mocks_verification(self, burger, mock_bun, mock_ingredient_sauce):
        """Тест проверки вызовов моков при получении чека"""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        burger.get_receipt()
        
        # Проверяем что методы были вызваны
        mock_bun.get_name.assert_called()
        mock_ingredient_sauce.get_type.assert_called_once()
        mock_ingredient_sauce.get_name.assert_called_once()
        mock_ingredient_sauce.get_price.assert_called_once()

    def test_complex_operations_sequence(self, burger, mock_bun, mock_ingredient_sauce, 
                                         mock_ingredient_filling, mock_ingredient_extra):
        """Тест последовательности сложных операций с бургером"""
        # 1. Устанавливаем булочку
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun
        
        # 2. Добавляем ингредиенты
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        burger.add_ingredient(mock_ingredient_extra)
        burger.add_ingredient(mock_ingredient_sauce)
        assert len(burger.ingredients) == 4
        
        # 3. Перемещаем ингредиенты
        burger.move_ingredient(0, 2)  # sauce -> после filling
        assert burger.ingredients[0] == mock_ingredient_filling
        assert burger.ingredients[1] == mock_ingredient_extra
        assert burger.ingredients[2] == mock_ingredient_sauce
        assert burger.ingredients[3] == mock_ingredient_sauce
        
        burger.move_ingredient(3, 1)  # sauce -> после extra
        assert burger.ingredients[0] == mock_ingredient_filling
        assert burger.ingredients[1] == mock_ingredient_sauce
        assert burger.ingredients[2] == mock_ingredient_extra
        assert burger.ingredients[3] == mock_ingredient_sauce
        
        # 4. Удаляем ингредиенты
        burger.remove_ingredient(2)  # удаляем extra
        assert len(burger.ingredients) == 3
        assert burger.ingredients[0] == mock_ingredient_filling
        assert burger.ingredients[1] == mock_ingredient_sauce
        assert burger.ingredients[2] == mock_ingredient_sauce
        
        burger.remove_ingredient(0)  # удаляем filling
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == mock_ingredient_sauce
        assert burger.ingredients[1] == mock_ingredient_sauce
        
        # 5. Проверяем цену
        mock_bun.get_price.return_value = 100
        mock_ingredient_sauce.get_price.return_value = 50
        expected_price = 100 * 2 + 50 + 50  # 300
        assert burger.get_price() == expected_price

    @pytest.mark.parametrize("operation, expected_result", [
        ("add", 1),
        ("remove", 0),
        ("move", 1),
    ])
    def test_operations_with_mocks(self, burger, mock_ingredient_sauce, operation, expected_result):
        """Тест различных операций с использованием моков"""
        if operation == "add":
            burger.add_ingredient(mock_ingredient_sauce)
            assert len(burger.ingredients) == expected_result
        elif operation == "remove":
            burger.add_ingredient(mock_ingredient_sauce)
            burger.remove_ingredient(0)
            assert len(burger.ingredients) == expected_result
        elif operation == "move":
            burger.add_ingredient(mock_ingredient_sauce)
            burger.add_ingredient(mock_ingredient_sauce)
            burger.move_ingredient(0, 1)
            assert len(burger.ingredients) == expected_result