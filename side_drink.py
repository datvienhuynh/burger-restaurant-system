class SideDrink():
	def __init__(self, name, type, size, price, calories, decrement_quantity=1):
		self._name = name
		self._type = type
		self._size = size
		self._price = price
		self._calories = calories
		self._decrement_quantity = decrement_quantity

	@property
	def name(self):
		return self._name

	@property
	def type(self):
		return self._type

	@property
	def size(self):
		return self._size

	@property
	def price(self):
		return self._price

	@property
	def calories(self):
		return self._calories
	
	@property
	def decrement_quantity(self):
		return self._decrement_quantity

	def __str__(self):
		return f'{self._type}: {self._name} < {self._size}, {self._calories} calories, ${self._price} >'
