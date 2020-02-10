from restaurant_system import RestaurantSystem
from ingredient import Ingredient
from side_drink import SideDrink
from inventory import Inventory
from main import Main, Burger, Wrap
from order import Order

def bootstrap_system():

	system = RestaurantSystem()

	''' Create menu '''
	bun_list = ['Bun', 'Sandwich']
	patty_list = ['Chicken Patty', 'Vegetarian Patty', 'Beef Patty']
	ingredient_list = ['Tomato', 'Lettuce', 'Tomato Sauce', 'Chili Sauce', 'Mayonnaise Sauce', 'Cheddar Cheese', 'Sweet Cheese']
	for name in bun_list:
		system.ingredients.append(Ingredient(name, 2, 300, 1))
		system.inventory.update_stock(Ingredient(name, 2, 300, 1),30)
	for name in patty_list:
		system.ingredients.append(Ingredient(name, 5, 600, 1))
		system.inventory.update_stock(Ingredient(name, 5, 600, 1),30)
	for name in ingredient_list:
		system.ingredients.append(Ingredient(name, 0.5, 50, 1))
		system.inventory.update_stock(Ingredient(name, 0.5, 50, 1),30)

	side_list1 = ['Nugget', 'Chips', 'Rice']
	side_list2 = ['Salad', 'Grilled Corn']
	contained_list = ['Water', 'Coca Cola', 'Fanta', 'Sprite', 'Sunkist']
	juice_list = ['Orange Juice', 'Watermelon', 'Pineapple', 'Apple']
	dessert_list = ['Chocolate Sundae', 'Strawberry Sundae']
	for name in side_list1:
		system.sides_drinks.append(SideDrink(name, 'Side', 'Small', 2, 200, 75))
		system.sides_drinks.append(SideDrink(name, 'Side', 'Medium', 2.5, 300, 125))
		system.sides_drinks.append(SideDrink(name, 'Side', 'Large', 3, 400, 175))
		system.inventory.update_stock(SideDrink(name, 'Side', 'Stock', 2, 200, 75), 1000)
	for name in side_list2:
		system.sides_drinks.append(SideDrink(name, 'Side', 'Small', 2, 100, 75))
		system.sides_drinks.append(SideDrink(name, 'Side', 'Medium', 2.5, 150, 125))
		system.sides_drinks.append(SideDrink(name, 'Side', 'Large', 3, 200, 175))
		system.inventory.update_stock(SideDrink(name, 'Side', 'Stock', 2, 100, 75), 1000)
	for name in contained_list:
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Can', 2, 100, 1))
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Bottle', 3, 200, 1))
		system.inventory.update_stock(SideDrink(name, 'Drink', 'Can', 2, 100, 1), 10)
		system.inventory.update_stock(SideDrink(name, 'Drink', 'Bottle', 3, 200, 1), 10)
	for name in juice_list:
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Small', 4, 150, 250))
		system.sides_drinks.append(SideDrink(name, 'Drink', 'Medium', 5, 200, 450))
		system.inventory.update_stock(SideDrink(name, 'Drink', 'Stock', 4, 150, 250), 2000)
	for name in dessert_list:
		system.sides_drinks.append(SideDrink(name, 'Dessert', 'Small', 3, 100, 50))
		system.sides_drinks.append(SideDrink(name, 'Dessert', 'Medium', 4, 150, 100))
		system.sides_drinks.append(SideDrink(name, 'Dessert', 'Large', 5, 200, 150))
		system.inventory.update_stock(SideDrink(name, 'Dessert', 'Stock', 2, 100, 50), 1000)

	''' Set base burgers and wraps '''
	single_burger = {}
	single_burger.update({system.search_ingredient('Bun'):2})
	single_burger.update({system.search_ingredient('Chicken Patty'):1})
	single_burger.update({system.search_ingredient('Tomato'):1})
	single_burger.update({system.search_ingredient('Lettuce'):1})
	single_burger.update({system.search_ingredient('Mayonnaise Sauce'):1})
	single_burger.update({system.search_ingredient('Cheddar Cheese'):1})
	system.add_base('Burger', single_burger)
	single_wrap = {}
	single_wrap.update({system.search_ingredient('Sandwich'):1})
	single_wrap.update({system.search_ingredient('Beef Patty'):1})
	single_wrap.update({system.search_ingredient('Tomato'):1})
	single_wrap.update({system.search_ingredient('Lettuce'):1})
	single_wrap.update({system.search_ingredient('Mayonnaise Sauce'):1})
	single_wrap.update({system.search_ingredient('Sweet Cheese'):1})
	system.add_base('Wrap', single_wrap)

	return system

