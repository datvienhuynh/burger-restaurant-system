from ingredient import Ingredient
from error import OrderError


class Main():
	def __init__(self, name, id, ingredients):
		self._name = name
		self._ingredients = {}
	
	def add_ingredient(self, ingredient, quantity):
		d1 = {ingredient:quantity}
		self._ingredients.update(d1)

	def calc_price(self):
		price = 0
		for ingredient, quantity in self._ingredients.items():
			price += ingredient.price * quantity
		return price

	def calc_calories(self):
		calor = 0
		for ingredient, quantity in self._ingredients.items():
			calor += ingredient.calories * quantity
		return calor
	
	def __str__(self):
		output = ''
		for ingredient, quantity in self._ingredients.items():
			output += f'< {ingredient.name}: {quantity} >\n'
		output += f'< ${str(self.calc_price())} >\n'
		return output
	
	'''
	Properties
	'''
	
	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, name):
		self._name = name
	
	'''
	@property
	def id(self):
		return self._id
	'''

	@property
	def ingredients(self):
		return self._ingredients

class Burger(Main):
	def __init__(self, id, ingredients, no_buns = 2):
		super().__init__('Burger', id, ingredients)
		self._no_buns = no_buns

	def __str__(self):
		return 'Burger: \n' + super().__str__()

class Wrap(Main):
	def __init__(self, id, ingredients, no_wraps = 1):
		super().__init__('Wrap', id, ingredients)
		self._no_wraps = no_wraps
	
	def __str__(self):
		return 'Wrap: \n' + super().__str__()
