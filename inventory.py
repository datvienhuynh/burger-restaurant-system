from ingredient import Ingredient
from side_drink import SideDrink

class Inventory():
	def __init__(self):
		self._stock = {}

	@property
	def stock(self):
		return self._stock
	
	def search_stock(self, name, size='Stock'):
		for item, qty in self._stock.items():
			if item.type != 'Ingredient':
				if item.name.lower() == name.lower() and item.size == size:
					return item
			elif item.name.lower() == name.lower():
				return item
		return None

	def is_in_stock(self, item):
		for key in self._stock.keys():
			if item.type == 'Drink' and (item.size == 'Bottle' or item.type == 'Can'):
				if item.name == key.name and item.size == key.size:
					if self._stock[key] >= item.decrement_quantity:
						return True
			else:
				if key.name == item.name:
					if self._stock[key] >= item.decrement_quantity:
						return True
		return False

	def is_sufficient(self, item, demand):
		for key in self._stock.keys():
			if item.type == 'Drink' and (item.size == 'Bottle' or item.type == 'Can'):
				if item.name == key.name and item.size == key.size:
					if self._stock[key] >= demand * item.decrement_quantity:
						return True
			else:
				if key.name == item.name:
					if self._stock[key] >= demand * item.decrement_quantity:
						return True
		return False

	def find_in_stock(self):
		in_stock = {}
		for item, qty in self._stock.items():
			if qty > 0:
				in_stock.update({item : qty})
		return in_stock

	def find_low_stock(self):
		low_stock = {}
		for item, qty in self._stock.items():
			if qty / item.decrement_quantity <= 10:
				low_stock.update({item : qty})
		return low_stock
				
	def find_low_stock_by_type(self, type):
		low_by_type = {}
		for item, qty in self.find_low_stock().items():
			if item.type.lower() == type.lower():
				low_by_type.update({item : qty})
		return low_by_type

	def update_stock(self, item, quantity):
		for key in self._stock.keys():
			if item.type == 'Drink' and (item.size == 'Bottle' or item.type == 'Can'):
				if item.name == key.name and item.size == key.size:
					self._stock[key] += quantity
					return
			else:
				if item.name == key.name:
					self._stock[key] += quantity
					return
		d1 = {item:quantity}
		self._stock.update(d1)
		
	def find_ingredient_quantity(self, name):
		for item in self._stock:
			if item.name == name:
				return self._stock[item]
		return 0

	def find_drink_quantity(self, name, size='Stock'):
		for item in self._stock:
			if item.name == name and item.size == size:
				return self._stock[item]
		return 0

	def __str__(self):
		pass
