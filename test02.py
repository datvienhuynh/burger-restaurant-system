from restaurant_system import RestaurantSystem
from ingredient import Ingredient
from order import Order
from main import Main, Burger, Wrap
from side_drink import SideDrink

import pytest

'''
	Test US7, US8
	regarding "Viewing Current Orders", "Updating Order Status"
'''

@pytest.fixture
def burger_fixture():
	system = RestaurantSystem()
	
	bun_list = ['Bun', 'Sandwich']
	patty_list = ['Chicken Patty', 'Vegetarian Patty', 'Beef Patty']
	ingredient_list = ['Tomato', 'Lettuce', 'Tomato Sauce', 'Chili Sauce', 'Mayonnaise Sauce', 'Cheddar Cheese', 'Sweet Cheese']
	for name in bun_list:
		system.ingredients.append(Ingredient(name, 2, 300, 1))
		system.inventory.update_stock(Ingredient(name, 2, 300, 1),300)
	for name in patty_list:
		system.ingredients.append(Ingredient(name, 5, 600, 1))
		system.inventory.update_stock(Ingredient(name, 5, 600, 1),200)
	for name in ingredient_list:
		system.ingredients.append(Ingredient(name, 0.5, 50, 1))
		system.inventory.update_stock(Ingredient(name, 0.5, 50, 1),100)
	
	side_list = ['Nugget', 'Chips', 'Salad', 'Rice', 'Grilled Corn']
	contained_list = ['Water', 'Coca Cola', 'Fanta', 'Sprite', 'Sunkist']
	juice_list = ['Orange Juice', 'Watermelon', 'Pineapple', 'Apple']
	for name in side_list:
		system.sides_drinks.append(SideDrink(name, 'Side', 'Small', 2, 200, 75))
		system.sides_drinks.append(SideDrink(name, 'Side', 'Medium', 2.5, 300, 125))
		system.sides_drinks.append(SideDrink(name, 'Side', 'Large', 3, 400, 175))
		system.inventory.update_stock(SideDrink(name, 'Side', 'Stock', 2, 200, 1), 5000)
	for name in contained_list:
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Can', 2, 100, 1))
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Bottle', 3, 200, 1))
		system.inventory.update_stock(SideDrink(name, 'Drink', 'Can', 2, 100, 1), 30)
		system.inventory.update_stock(SideDrink(name, 'Drink', 'Bottle', 3, 200, 1), 30)
	for name in juice_list:
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Small', 4, 150, 250))
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Medium', 5, 200, 450))
		system.inventory.update_stock(SideDrink(name, 'Drink', 'Stock', 4, 150, 400), 3000)
	
	return system

def test_view_current_orders(burger_fixture):
	print('Test viewing current orders')
	
	mains1 = []
	ingredients1 = {}
	ingredients1.update({burger_fixture.search_ingredient('Bun'):2})
	ingredients1.update({burger_fixture.search_ingredient('Chicken Patty'):2})
	ingredients1.update({burger_fixture.search_ingredient('Tomato'):1})
	ingredients1.update({burger_fixture.search_ingredient('Lettuce'):1})
	ingredients1.update({burger_fixture.search_ingredient('Tomato Sauce'):1})
	ingredients1.update({burger_fixture.search_ingredient('Cheddar Cheese'):1})
	mains1.append(burger_fixture.create_main('Burger', ingredients1))
	
	mains2 = []
	ingredients2 = {}
	ingredients2.update({burger_fixture.search_ingredient('Sandwich'):1})
	ingredients2.update({burger_fixture.search_ingredient('Beef Patty'):2})
	ingredients2.update({burger_fixture.search_ingredient('Tomato'):2})
	ingredients2.update({burger_fixture.search_ingredient('Lettuce'):1})
	ingredients2.update({burger_fixture.search_ingredient('Chili Sauce'):1})
	ingredients2.update({burger_fixture.search_ingredient('Sweet Cheese'):2})
	mains2.append(burger_fixture.create_main('Wrap', ingredients2))
	
	sides_drinks = []
	sides_drinks.append(burger_fixture.search_sides_drinks('Fanta', 'Bottle'))
	sides_drinks.append(burger_fixture.search_sides_drinks('Chips', 'Large'))
	
	burger_fixture.make_order(mains1, sides_drinks)
	burger_fixture.make_order(mains2, sides_drinks)
	assert len(burger_fixture.orders) == 2
	assert burger_fixture.orders[0] in burger_fixture.get_current_order()
	assert burger_fixture.orders[1] in burger_fixture.get_current_order()
	order = burger_fixture.get_current_order()[0]
	assert order.id == 1
	assert sides_drinks == order.sides_drinks
	burger_fixture.update_status(1)
	burger_fixture.update_status(1)
	burger_fixture.update_status(1)
	assert burger_fixture.orders[0] not in burger_fixture.get_current_order()
	assert burger_fixture.orders[1] in burger_fixture.get_current_order()

def test_new_order_status(burger_fixture):
	print('Test a new order status')
	
	mains1 = []
	ingredients1 = {}
	ingredients1.update({burger_fixture.search_ingredient('Bun'):2})
	ingredients1.update({burger_fixture.search_ingredient('Chicken Patty'):2})
	ingredients1.update({burger_fixture.search_ingredient('Tomato'):1})
	ingredients1.update({burger_fixture.search_ingredient('Lettuce'):1})
	ingredients1.update({burger_fixture.search_ingredient('Tomato Sauce'):1})
	ingredients1.update({burger_fixture.search_ingredient('Cheddar Cheese'):1})
	mains1.append(burger_fixture.create_main('Burger', ingredients1))
	
	mains2 = []
	ingredients2 = {}
	ingredients2.update({burger_fixture.search_ingredient('Sandwich'):1})
	ingredients2.update({burger_fixture.search_ingredient('Beef Patty'):2})
	ingredients2.update({burger_fixture.search_ingredient('Tomato'):2})
	ingredients2.update({burger_fixture.search_ingredient('Lettuce'):1})
	ingredients2.update({burger_fixture.search_ingredient('Chili Sauce'):1})
	ingredients2.update({burger_fixture.search_ingredient('Sweet Cheese'):2})
	mains2.append(burger_fixture.create_main('Wrap', ingredients2))
	
	sides_drinks = []
	sides_drinks.append(burger_fixture.search_sides_drinks('Fanta', 'Bottle'))
	sides_drinks.append(burger_fixture.search_sides_drinks('Chips', 'Large'))
	
	burger_fixture.make_order(mains1, sides_drinks)
	burger_fixture.make_order(mains2, sides_drinks)
	assert len(burger_fixture.orders) == 2
	assert burger_fixture.orders[0].status == 'Queueing'
	assert burger_fixture.orders[1].status == 'Queueing'

def test_update_order_status(burger_fixture):
	print('Test updating an order status')
	
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
	assert len(burger_fixture.orders) == 1
	assert burger_fixture.orders[0].status == 'Queueing'
	burger_fixture.update_status(1)
	assert burger_fixture.orders[0].status == 'Preparing'
	burger_fixture.update_status(1)
	assert burger_fixture.orders[0].status == 'Ready to collect'
	burger_fixture.update_status(1)
	assert burger_fixture.orders[0].status == 'Collected'

def test_prepared_order(burger_fixture):
	print('Test updating a prepared order')
	
	mains1 = []
	ingredients1 = {}
	ingredients1.update({burger_fixture.search_ingredient('Bun'):2})
	ingredients1.update({burger_fixture.search_ingredient('Chicken Patty'):2})
	ingredients1.update({burger_fixture.search_ingredient('Tomato'):1})
	ingredients1.update({burger_fixture.search_ingredient('Lettuce'):1})
	ingredients1.update({burger_fixture.search_ingredient('Tomato Sauce'):1})
	ingredients1.update({burger_fixture.search_ingredient('Cheddar Cheese'):1})
	mains1.append(burger_fixture.create_main('Burger', ingredients1))
	
	mains2 = []
	ingredients2 = {}
	ingredients2.update({burger_fixture.search_ingredient('Sandwich'):1})
	ingredients2.update({burger_fixture.search_ingredient('Beef Patty'):2})
	ingredients2.update({burger_fixture.search_ingredient('Tomato'):2})
	ingredients2.update({burger_fixture.search_ingredient('Lettuce'):1})
	ingredients2.update({burger_fixture.search_ingredient('Chili Sauce'):1})
	ingredients2.update({burger_fixture.search_ingredient('Sweet Cheese'):2})
	mains2.append(burger_fixture.create_main('Wrap', ingredients2))
	
	sides_drinks = []
	sides_drinks.append(burger_fixture.search_sides_drinks('Fanta', 'Bottle'))
	sides_drinks.append(burger_fixture.search_sides_drinks('Chips', 'Large'))
	
	burger_fixture.make_order(mains1, sides_drinks)
	burger_fixture.make_order(mains2, sides_drinks)
	assert len(burger_fixture.orders) == 2
	assert burger_fixture.orders[0].status == 'Queueing'
	assert burger_fixture.orders[1].status == 'Queueing'
	burger_fixture.update_status(2)
	burger_fixture.update_status(2)
	burger_fixture.update_status(2)
	assert burger_fixture.orders[1].status == 'Collected'
	assert burger_fixture.orders[1] not in burger_fixture.get_current_order()
