from inventory import Inventory
from order import Order
from ingredient import Ingredient
from main import Main, Burger, Wrap
from side_drink import SideDrink
from error import OrderError, InvalidIDError, check_id_error, check_order_error
from datetime import datetime


class RestaurantSystem():
	def __init__(self):
		self._bases = []
		self._ingredients = []
		self._sides_drinks = []
		self._orders = []
		self._inventory = Inventory()
	
	'''
	Registration Services
	'''
	
	def add_base(self, mainType, ingredients):
		self._bases.append(self.create_main(mainType, ingredients))
	
	def get_base_by_name(self, name):
		for base in self._bases:
			if base.name == name:
				return base
		return None
	
	def search_ingredient(self, name):
		for ingredient in self._ingredients:
			if name.lower() == ingredient.name.lower():
				return ingredient
		return None
	
	def add_ingredient(self, name, price, calories, decrement_quantity=1, stock_quantity=0):
		if self.search_ingredient(name) != None:
			return None
		ingredient = Ingredient(name, price, calories, decrement_quantity)
		self._ingredients.append(ingredient)
		self._inventory.stock.update({ingredient : stock_quantity})
		return ingredient
	
	def remove_ingredient(self, name):
		for ingredient in self._ingredients:
			if name.lower() == ingredient.name.lower():
				self._ingredients.remove(ingredient)
		for item in self._inventory.stock.keys():
			if item.name.lower() == name.lower() and item.type == 'Ingredient':
				self._inventory.stock.pop(item, None)
				return

	def search_sides_drinks(self, name, size):
		for side_drink in self._sides_drinks:
			if name.lower() == side_drink.name.lower() and size.lower() == side_drink.size.lower():
				return side_drink
		return None
	
	def add_side_drink(self, name, type, size, price, calories, decrement_quantity=1):
		if self.search_sides_drinks(name, size) != None:
			return None
		side_drink = SideDrink(name, type, size, price, calories, decrement_quantity)
		self._sides_drinks.append(side_drink)
		return side_drink
	
	def remove_side_drink(self, name, size='Stock'):
		if size == 'Can' or size == 'Bottle':
			for item in self._sides_drinks:
				if item.name == name and item.size == size:
					self._sides_drinks.remove(item)
			for item in self._inventory.stock.keys():
				if item.name == name and item.size == size:
					self._inventory.stock.pop(item, None)
					return
		else:
			for item in self._sides_drinks:
				if item.name == name:
					self._sides_drinks.remove(item)
			for item in self._inventory.stock.keys():
				if item.name == name:
					self._inventory.stock.pop(item, None)
					return

	def get_all_ingredients(self):
		ingredients = {}
		for ingredient, qty in self._inventory.stock.items():
			if ingredient.type == 'Ingredient':
				ingredients.update({ingredient : qty})
		return ingredients
	
	def get_all_sides(self):
		sides = {}
		for side, qty in self._inventory.stock.items():
			if side.type == 'Side':
				sides.update({side : qty})
		return sides
				
	def get_all_drinks(self):
		drinks = {}
		for drink, qty in self._inventory.stock.items():
			if drink.type == 'Drink':
				drinks.update({drink : qty})
		return drinks

	def get_all_desserts(self):
		desserts = {}
		for dessert, qty in self._inventory.stock.items():
			if dessert.type == 'Dessert':
				desserts.update({dessert : qty})
		return desserts

	'''
	Order Services
	'''
	
	def search_order(self, id):
		try:
			if check_id_error(id, self._orders) != True:
				raise InvalidIDError()
			for order in self._orders:
				if order.id == id:
					return order
		except InvalidIDError as error:
			return error.mesg
	
	def make_order(self, mains, sides_drinks):
		if len(self._orders) == 0:
			id = 1
		else:
			lastOrder = self._orders[-1]
			id = int(lastOrder.id) + 1
		order_time = datetime.now()
		order = Order(id, mains, sides_drinks, order_time.strftime("%Y-%m-%d %H:%M:%S"))
		self._orders.append(order)
		
		for main in mains:
			for ingredient, quantity in main.ingredients.items():
				minus = - quantity * ingredient.decrement_quantity
				self._inventory.update_stock(ingredient, minus)
		for side_drink in sides_drinks:
			minus = - side_drink.decrement_quantity
			self._inventory.update_stock(side_drink, minus)
		
		return id
	
	def calc_net_price(self, mains, sides_drinks):
		stock = self._inventory
		
		error = check_order_error(mains, sides_drinks, stock)
		if len(error) > 0:
			raise OrderError(error)

		
		total = 0
		for main in mains:
			total += main.calc_price()
		for side_drink in sides_drinks:
			total += side_drink.price
		return total
	
	def create_main(self, mainType, ingredients):
		if mainType == "Burger":
			main = Burger(1,{})
		else:
			main = Wrap(1,{})
		for ingredient, quantity in ingredients.items():
				main.add_ingredient(ingredient,quantity)
		return main

	def validate_inputs(self, mains, sides_drinks):
		stock = self._inventory
		
		error = check_order_error(mains, sides_drinks, stock)

		return error

	def check_order_status(self, id):
		try:
			if check_id_error(id, self._orders) != True:
				raise InvalidIDError(check_id_error(id, self._orders).mesg)
			
			for order in self._orders:
				if order.id == id:
					return order.status
	
		except InvalidIDError as error:
			return error.mesg
	
	def update_status(self, id):
		order = self.search_order(id)
		if order.status == 'Queueing':
			order.status = 'Preparing'
		elif order.status == 'Preparing':
			order.status = 'Ready to collect'
		else:
			order.status = 'Collected'
	
	def remove_order(self, id):
		for order in self._orders:
			if order.id == id:
				self._orders.remove(order)

	def get_current_order(self):
		current_orders = []
		for order in self._orders:
			if order.status != 'Collected':
				current_orders.append(order)
		return current_orders

	def is_negative_stock(self, mains, sides_drinks):
		stock = self._inventory.stock.copy()
		
		for main in mains:
			for ingredient, quantity in main.ingredients.items():
				for key in stock.keys():
					if ingredient.name == key.name:
						stock[key] -= quantity * ingredient.decrement_quantity

		for side_drink in sides_drinks:
			for key in stock.keys():
				if side_drink.type == 'Drink' and (side_drink.size == 'Bottle' or side_drink.type == 'Can'):
					if side_drink.name == key.name and side_drink.size == key.size:
						stock[key] -= side_drink.decrement_quantity
				else:
					if side_drink.name == key.name:
						stock[key] -= side_drink.decrement_quantity

		for qty in stock.values():
			if qty < 0:
				return True
		return False

	'''
	Get menus
	'''

	def get_ingredient_menu(self):
		ingredient_menu = []
		for ingredient in self._ingredients:
			if self._inventory.is_in_stock(ingredient) == True:
				ingredient_menu.append(ingredient)
		return ingredient_menu
	
	def get_base_menu(self):
		base_menu = []
		for base in self._bases:
			check = True
			for ingredient, quantity in base.ingredients.items():
				if self._inventory.is_sufficient(ingredient, quantity) == False:
					check = False
					break
			if check == False:
				break
			base_menu.append(base)
		return base_menu

	def get_side_menu(self):
		side_menu = []
		for side in self._sides_drinks:
			if side.type == 'Side' and self._inventory.is_in_stock(side) == True:
				side_menu.append(side)
		return side_menu

	def get_drink_menu(self):
		drink_menu = []
		for drink in self._sides_drinks:
			if drink.type == 'Drink' and self._inventory.is_in_stock(drink) == True:
				drink_menu.append(drink)
		return drink_menu

	def get_dessert_menu(self):
		dessert_menu = []
		for dessert in self._sides_drinks:
			if dessert.type == 'Dessert' and self._inventory.is_in_stock(dessert) == True:
				dessert_menu.append(dessert)
		return dessert_menu

	'''
	Properties
	'''
	
	@property
	def bases(self):
		return self._bases
	
	@property
	def ingredients(self):
		return self._ingredients
	
	@property
	def sides_drinks(self):
		return self._sides_drinks
	
	@property
	def orders(self):
		return self._orders
	
	@property
	def inventory(self):
		return self._inventory

