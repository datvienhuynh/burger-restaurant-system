class Ingredient():
	def __init__(self, name, price, calories, decrement_quantity=1):
		self._name = name
		self._price = price
		self._calories = calories
		self._decrement_quantity = decrement_quantity
		self._type = 'Ingredient'

	@property
	def name(self):
		return self._name

	@property
	def price(self):
		return self._price

	@property
	def calories(self):
		return self._calories

	@property
	def type(self):
		return self._type
	
	@property
	def decrement_quantity(self):
		return self._decrement_quantity

	def __str__(self):
		return f'Ingredient: <name: {self._name}, price: {self._price} dollars, calories: {self._calories}>'
