from ingredient import Ingredient
from main import Main, Burger, Wrap
from side_drink import SideDrink
from datetime import datetime


class Order():
	def __init__(self, id, mains, sides_drinks, order_time, status = 'Queueing'):
		self._id = id
		self._mains = mains
		self._sides_drinks = sides_drinks
		self._order_time = order_time
		self._status = status
	
	@property
	def id(self):
		return self._id

	@property
	def mains(self):
		return self._mains

	def add_main(self, main):
		self._mains.append(main)

	@property
	def sides_drinks(self):
		return self._sides_drinks

	@property
	def order_time(self):
		return self._order_time
	
	@property
	def status(self):
		return self._status
	@status.setter
	def status(self, status):
		self._status = status
	
	def __str__(self):
		return f'Order <{self._id}: {self._status}>\nTotal: {self.calc_price()}\nOrder at: {self._order_time}'

	def calc_price(self):
		total = 0
		for main in self._mains:
			total += main.calc_price()
		for side_drink in self._sides_drinks:
			total += side_drink.price
		return total

	def calc_calories(self):
		calor = 0
		for main in self._mains:
			total += main.calc_calories()
		for side_drink in self._sides_drinks:
			total += side_drink.calories
		return calor

