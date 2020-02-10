from restaurant_system import RestaurantSystem
from ingredient import Ingredient
from order import Order
from main import Main, Burger, Wrap
from side_drink import SideDrink
from error import OrderError, check_order_error
from inventory import Inventory

import pytest

'''
	Test US9, US10, US11, US12
	regarding "Checking - Updating inventory", "Creating - Deleting Ingredients"
'''

@pytest.fixture
def burger_fixture():
	system = RestaurantSystem()
	
	bun_list = ['Bun', 'Sandwich']
	patty_list = ['Chicken Patty', 'Vegetarian Patty', 'Beef Patty']
	ingredient_list = ['Tomato', 'Lettuce', 'Tomato Sauce', 'Chili Sauce', 'Mayonnaise Sauce', 'Cheddar Cheese', 'Sweet Cheese']
	for name in bun_list:
		system.ingredients.append(Ingredient(name, 2, 300, 1))
		system.inventory.update_stock(Ingredient(name, 2, 300, 1),20)
	for name in patty_list:
		system.ingredients.append(Ingredient(name, 5, 600, 1))
		system.inventory.update_stock(Ingredient(name, 5, 600, 1),20)
	for name in ingredient_list:
		system.ingredients.append(Ingredient(name, 0.5, 50, 1))
		system.inventory.update_stock(Ingredient(name, 0.5, 50, 1),20)
	
	side_list = ['Nugget', 'Chips', 'Salad', 'Rice', 'Grilled Corn']
	contained_list = ['Water', 'Coca Cola', 'Fanta', 'Sprite', 'Sunkist']
	juice_list = ['Orange Juice', 'Watermelon', 'Pineapple', 'Apple']
	for name in side_list:
		system.sides_drinks.append(SideDrink(name, 'Side', 'Small', 2, 200, 75))
		system.sides_drinks.append(SideDrink(name, 'Side', 'Medium', 2.5, 300, 125))
		system.sides_drinks.append(SideDrink(name, 'Side', 'Large', 3, 400, 175))
		system.inventory.update_stock(SideDrink(name, 'Side', 'Stock', 2, 200, 75), 2000)
	for name in contained_list:
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Can', 2, 100, 1))
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Bottle', 3, 200, 1))
		system.inventory.update_stock(SideDrink(name, 'Drink', 'Can', 2, 100, 1), 20)
		system.inventory.update_stock(SideDrink(name, 'Drink', 'Bottle', 3, 200, 1), 20)
	for name in juice_list:
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Small', 4, 150, 250))
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Medium', 5, 200, 450))
		system.inventory.update_stock(SideDrink(name, 'Drink', 'Stock', 4, 150, 250), 3000)
	
	return system

def test_check_quantity(burger_fixture):
	print('Test checking the quantity of ingredients')
	
	bun_list = ['Bun', 'Sandwich']
	patty_list = ['Chicken Patty', 'Vegetarian Patty', 'Beef Patty']
	ingredient_list = ['Tomato', 'Lettuce', 'Tomato Sauce', 'Chili Sauce', 'Mayonnaise Sauce', 'Cheddar Cheese', 'Sweet Cheese']
	side_list = ['Nugget', 'Chips', 'Salad', 'Rice', 'Grilled Corn']
	contained_list = ['Water', 'Coca Cola', 'Fanta', 'Sprite', 'Sunkist']
	juice_list = ['Orange Juice', 'Watermelon', 'Pineapple', 'Apple']

	for name in bun_list:
		assert burger_fixture.inventory.find_ingredient_quantity(name) == 20
	for name in patty_list:
		assert burger_fixture.inventory.find_ingredient_quantity(name) == 20
	for name in ingredient_list:
		assert burger_fixture.inventory.find_ingredient_quantity(name) == 20
	for name in side_list:
		assert burger_fixture.inventory.find_ingredient_quantity(name) == 2000
	for name in contained_list:
		assert burger_fixture.inventory.find_drink_quantity(name, 'Can') == 20
		assert burger_fixture.inventory.find_drink_quantity(name, 'Bottle') == 20
	for name in juice_list:
		assert burger_fixture.inventory.find_drink_quantity(name) == 3000
		assert burger_fixture.inventory.find_drink_quantity(name) == 3000

def test_check_low_stock(burger_fixture):
	print('Test checking the low stock ingredients')
	
	assert len(burger_fixture.inventory.find_low_stock()) == 0
	bun = burger_fixture.inventory.search_stock('Bun')
	burger_fixture.inventory.update_stock(bun, -10)
	chips = burger_fixture.inventory.search_stock('Chips')
	burger_fixture.inventory.update_stock(chips, -1500)
	fanta = burger_fixture.inventory.search_stock('Fanta', 'Bottle')
	burger_fixture.inventory.update_stock(fanta, -10)
	low_stock = burger_fixture.inventory.find_low_stock()
	assert len(low_stock) == 3
	assert bun in low_stock and low_stock[bun] == 10
	assert chips in low_stock and low_stock[chips] == 500
	assert fanta in low_stock and low_stock[fanta] == 10

def test_update_stock(burger_fixture):
	print('Test updating stock')

	stock = burger_fixture.inventory.stock
	bun = burger_fixture.inventory.search_stock('Bun')
	assert stock[bun] == 20
	burger_fixture.inventory.update_stock(bun, 10)
	assert stock[bun] == 30
	
	chips = burger_fixture.inventory.search_stock('Chips')
	assert stock[chips] == 2000
	burger_fixture.inventory.update_stock(chips, 1000)
	assert stock[chips] == 3000
	
	fanta = burger_fixture.inventory.search_stock('Fanta', 'Bottle')
	assert stock[fanta] == 20
	burger_fixture.inventory.update_stock(fanta, 10)
	assert stock[fanta] == 30

	mains1 = []
	ingredients1 = {}
	ingredients1.update({burger_fixture.search_ingredient('Bun'):2})
	ingredients1.update({burger_fixture.search_ingredient('Chicken Patty'):2})
	ingredients1.update({burger_fixture.search_ingredient('Tomato'):1})
	ingredients1.update({burger_fixture.search_ingredient('Lettuce'):1})
	ingredients1.update({burger_fixture.search_ingredient('Tomato Sauce'):1})
	ingredients1.update({burger_fixture.search_ingredient('Cheddar Cheese'):1})
	mains1.append(burger_fixture.create_main('Burger', ingredients1))
	sides_drinks = []
	sides_drinks.append(burger_fixture.search_sides_drinks('Fanta', 'Bottle'))
	sides_drinks.append(burger_fixture.search_sides_drinks('Chips', 'Large'))
	burger_fixture.make_order(mains1, sides_drinks)
	assert stock[bun] == 28
	assert stock[chips] == 2825
	assert stock[fanta] == 29

def test_check_adding_ingredient(burger_fixture):
	print('Test checking adding a new ingredient')

	assert len(burger_fixture.get_ingredient_menu()) == 12
	assert len(burger_fixture.inventory.stock) == 31

	mushroom = burger_fixture.add_ingredient('Mushroom', 0.5, 30, 1, 20)
	assert len(burger_fixture.get_ingredient_menu()) == 13
	assert len(burger_fixture.inventory.stock) == 32
	assert mushroom in burger_fixture.get_ingredient_menu()
	assert mushroom in burger_fixture.inventory.stock
	assert burger_fixture.inventory.stock[mushroom] == 20

def test_check_removing_ingredient(burger_fixture):
	print('Test checking removing an ingredient')
	
	assert len(burger_fixture.get_ingredient_menu()) == 12
	assert len(burger_fixture.inventory.stock) == 31

	burger_fixture.remove_ingredient('Bun')
	burger_fixture.remove_side_drink('Chips')
	burger_fixture.remove_side_drink('Fanta', 'Bottle')
	assert len(burger_fixture.get_ingredient_menu()) == 11
	assert len(burger_fixture.inventory.stock) == 28
	assert burger_fixture.search_ingredient('Bun') == None
	assert burger_fixture.inventory.search_stock('Bun') == None
	assert burger_fixture.search_sides_drinks('Chips', 'Small') == None
	assert burger_fixture.inventory.search_stock('Chips') == None
	assert burger_fixture.search_sides_drinks('Fanta', 'Bottle') == None
	assert burger_fixture.inventory.search_stock('Fanta', 'Bottle') == None
