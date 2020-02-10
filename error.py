class OrderError(Exception):
	def __init__(self, errors):
		self.errors = errors

	def __str__(self):
		msg = ""

		for error in self.errors.values():
			msg += f"{error}\n"
		
		return msg

def check_order_error(mains, sides_drinks, stock):
	error = {}
	
	for main in mains:
		bunQuantity = 0
		sandQuantity = 0
		for ingredient, quantity in main.ingredients.items():
			if ingredient.name == "Bun":
				bunQuantity = quantity
			elif ingredient.name == "Sandwich":
				sandQuantity = quantity
			if quantity > 10:
				error["invalid_input_{0}".format(ingredient.name)] = f"Sorry, please enter {ingredient.name} amount between 0 and 10."
		for ingredient, quantity in main.ingredients.items():
			if stock.is_sufficient(ingredient, quantity) == False:
				error[ingredient.name] = f"Sorry, not enough stock for {ingredient.name}."
			elif bunQuantity > 0 and (ingredient.name in ("Chicken Patty", "Beef Patty", "Vegetarian Patty")) and (quantity > (bunQuantity-1) * 2):
				error["invalid_patties"] = "Sorry, please enter number of {2} between {0} to {1}.".format(bunQuantity-1,(bunQuantity-1)*2,ingredient.name)
			elif sandQuantity > 0 and (ingredient.name in ("Chicken Patty", "Beef Patty", "Vegetarian Patty")) and (quantity > 2):
				error["invalid_patties"] = "Sorry, please enter number of {2} between {0} to {1}.".format(1,2,ingredient.name)
	for side_drink in sides_drinks:
		if stock.is_sufficient(side_drink, 1) == False:
			error[side_drink.name] = f"Sorry, not enough stock for {side_drink.name}."
	
	return error
	

class InvalidIDError(Exception):
	def __init__(self, mesg):
		self.mesg = mesg

def check_id_error(id, orders):
	error = InvalidIDError('')
	if id is None or id == '':
		error.mesg = 'Type in a valid order ID'
	else:
		for order in orders:
			if order.id == id:
				return True
		error.mesg = 'Your order no longer exists'
	return error
