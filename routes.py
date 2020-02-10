from flask import render_template, request, redirect, url_for, abort
from server import app, system, mains, sides_drinks, total_price
from datetime import datetime
from ingredient import Ingredient
from side_drink import SideDrink
from inventory import Inventory
from main import Main, Burger, Wrap
from order import Order
from pickle_system import save_data

''' Page not found '''
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
	return render_template('404.html'), 404

''' Home page '''
@app.route('/', methods=["GET", "POST"])
def home():

	if request.method == "POST":

		global mains
		global sides_drinks
		global total_price

		if 'check_id' in request.form:
			if 'order_id' in request.form:
				if request.form['order_id'].isdigit() != True:
					return render_template('home.html', check='check_id', error='Type in a valid ID')
				id = int(request.form['order_id'])
				return render_template('home.html', status=system.check_order_status(id))
			return render_template('home.html', check='check_id')

		elif 'base_order' in request.form:
			if total_price != 0:
				return render_template('home.html', base_menu=system.get_base_menu(), side_menu=system.get_side_menu(), drink_menu=system.get_drink_menu(), dessert_menu=system.get_dessert_menu(), mains=mains, sides_drinks=sides_drinks, total=total_price)
			return render_template('home.html', base_menu=system.bases, side_menu=system.get_side_menu(), drink_menu=system.get_drink_menu(), dessert_menu=system.get_dessert_menu())

		elif 'make_order' in request.form:
			if system.is_negative_stock(mains, sides_drinks) == True:
				mains = []
				sides_drinks = []
				total_price = 0
				return render_template('home.html', check_out_error='Sorry, your order exceeds the stock')
			return render_template('home.html', mains=mains, sides_drinks=sides_drinks, total=total_price)

		elif 'clear_order' in request.form:
			mains = []
			sides_drinks = []
			total_price = 0
			return render_template('home.html')

		elif 'checkout' in request.form:
			id = system.make_order(mains, sides_drinks)
			save_data(system)
			mains = []
			sides_drinks = []
			total_price = 0
			return render_template('order_confirm.html', id=id)

		elif 'add_base' in request.form:
			burger_qty = int(request.form['Burger'])
			wrap_qty = int(request.form['Wrap'])
			for i in range(0, burger_qty):
				mains.append(system.get_base_by_name('Burger'))
			for i in range(0, wrap_qty):
				mains.append(system.get_base_by_name('Wrap'))
			total_price = system.calc_net_price(mains, sides_drinks)
			return render_template('home.html', base_menu=system.bases, side_menu=system.get_side_menu(), drink_menu=system.get_drink_menu(), dessert_menu=system.get_dessert_menu(), mains=mains, sides_drinks=sides_drinks, total=total_price)

		elif 'add_sides_base' in request.form:
			for key, qty in request.form.items():
				pair = key.split('_',1)
				if len(pair) == 2:
					name = pair[0]
					size = pair[1]
					if system.search_sides_drinks(name, size) != None and int(qty) > 0:
						for i in range(0, int(qty)):
							sides_drinks.append(system.search_sides_drinks(name, size))
			total_price = system.calc_net_price(mains, sides_drinks)
			return render_template('home.html', base_menu=system.get_base_menu(), side_menu=system.get_side_menu(), drink_menu=system.get_drink_menu(), dessert_menu=system.get_dessert_menu(), mains=mains, sides_drinks=sides_drinks, total=total_price)

		elif 'custom_order' in request.form:
			
			ingredient_qty = {}
			ingredients = system.get_ingredient_menu()
			for item in ingredients:
				ingredient_qty[item.name] = 0
			
			sides_qty = {}
			sides_name = {}
			sides = system.get_side_menu()
			for item in sides:
				name = f"{item.name}_{item.size}"
				sides_name[item] = name
				sides_qty[name] = 0

			drinks_qty = {}
			drinks_name = {}
			drinks = system.get_drink_menu()
			for item in drinks:
				name = f"{item.name}_{item.size}"
				drinks_name[item] = name
				drinks_qty[name] = 0
			
			desserts_qty = {}
			desserts_name = {}
			desserts = system.get_dessert_menu()
			for item in desserts:
				name = f"{item.name}_{item.size}"
				desserts_name[item] = name
				desserts_qty[name] = 0

			if total_price != 0:
				return render_template('home.html', ingredient_menu=system.get_ingredient_menu(), mains=mains, sides_drinks=sides_drinks, total=total_price, ingredient_qty=ingredient_qty, sides_qty=sides_qty, 
				drinks_qty=drinks_qty, desserts_qty=desserts_qty, sides_name=sides_name, drinks_name=drinks_name, desserts_name=desserts_name, canClear=True)
			return render_template('home.html', ingredient_menu=system.get_ingredient_menu(), ingredient_qty=ingredient_qty, sides_qty=sides_qty, 
			drinks_qty=drinks_qty, desserts_qty=desserts_qty, sides_name=sides_name, drinks_name=drinks_name, desserts_name=desserts_name)

		elif 'add_custom' in request.form:
			ingredient_qty = {}
			ingredients = system.get_ingredient_menu()
			for item in ingredients:
				ingredient_qty[item.name] = request.form[item.name]
			
			sides_qty = {}
			sides_name = {}
			sides = system.get_side_menu()
			for item in sides:
				name = f"{item.name}_{item.size}"
				sides_name[item] = name
				sides_qty[name] = request.form[name]
				
			drinks_qty = {}
			drinks_name = {}
			drinks = system.get_drink_menu()
			for item in drinks:
				name = f"{item.name}_{item.size}"
				drinks_name[item] = name
				drinks_qty[name] = request.form[name]
			
			desserts_qty = {}
			desserts_name = {}
			desserts = system.get_dessert_menu()
			for item in desserts:
				name = f"{item.name}_{item.size}"
				desserts_name[item] = name
				desserts_qty[name] = request.form[name]
			
			if int(request.form['Bun']) == 0 and int(request.form['Sandwich']) == 0:
				return render_template('home.html', ingredient_menu=system.get_ingredient_menu(), error = "Please specify base type.(Bun or Sandwich)", 
				ingredient_qty=ingredient_qty, sides_qty=sides_qty, drinks_qty=drinks_qty, desserts_qty=desserts_qty, sides_name=sides_name, drinks_name=drinks_name, 
				desserts_name=desserts_name)
			if int(request.form['Bun']) > 0 and int(request.form['Sandwich']) > 0:
				return render_template('home.html', ingredient_menu=system.get_ingredient_menu(), error = "Please only choose 1 base type.(Bun or Sandwich)", 
				ingredient_qty=ingredient_qty, sides_qty=sides_qty, drinks_qty=drinks_qty, desserts_qty=desserts_qty, sides_name=sides_name, drinks_name=drinks_name, 
				desserts_name=desserts_name)

			if int(request.form['Bun']) > 0:
				mainType = 'Burger'
			else:
				mainType = 'Wrap'

			ingredients = {}

			for name, qty in request.form.items():
				if system.search_ingredient(name) != None and int(qty) > 0:
					ingredients[system.search_ingredient(name)] = int(qty)

			tempMain = []
			tempSD = []
			tempMain.append(system.create_main(mainType,ingredients))
			errorList = system.validate_inputs(tempMain,tempSD)

			if len(errorList) > 0:
				return render_template('home.html', ingredient_menu=system.get_ingredient_menu(), errorList = errorList, ingredient_qty=ingredient_qty, 
				sides_name=sides_name, sides_qty=sides_qty, drinks_qty=drinks_qty, drinks_name=drinks_name, desserts_name=desserts_name, desserts_qty=desserts_qty)
			else:
				for key in ingredient_qty.keys():
					ingredient_qty[key] = 0
				for key in sides_qty.keys():
					sides_qty[key] = 0
				for key in drinks_qty.keys():
					drinks_qty[key] = 0
				for key in desserts_qty.keys():
					desserts_qty[key] = 0
				mains.append(system.create_main(mainType, ingredients))
				total_price = system.calc_net_price(mains, sides_drinks)
				return render_template('home.html', ingredient_menu=system.get_ingredient_menu(), ingredient_qty=ingredient_qty, sides_name=sides_name, sides_qty=sides_qty,
				drinks_name=drinks_name, drinks_qty=drinks_qty, desserts_name=desserts_name, desserts_qty=desserts_qty, mains=mains, sides_drinks=sides_drinks, total=total_price)

		elif 'add_sides' in request.form or 'add_drinks' in request.form or 'add_dessert' in request.form:
			ingredient_qty = {}
			ingredients = system.get_ingredient_menu()
			for item in ingredients:
				ingredient_qty[item.name] = request.form[item.name]
			
			sides_qty = {}
			sides_name = {}
			sides = system.get_side_menu()
			for item in sides:
				name = f"{item.name}_{item.size}"
				sides_name[item] = name
				sides_qty[name] = request.form[name]
				
			drinks_qty = {}
			drinks_name = {}
			drinks = system.get_drink_menu()
			for item in drinks:
				name = f"{item.name}_{item.size}"
				drinks_name[item] = name
				drinks_qty[name] = request.form[name]
			
			desserts_qty = {}
			desserts_name = {}
			desserts = system.get_dessert_menu()
			for item in desserts:
				name = f"{item.name}_{item.size}"
				desserts_name[item] = name
				desserts_qty[name] = request.form[name]

			tempMain = []
			tempSD = []
			for key, qty in request.form.items():
				pair = key.split('_',1)
				if len(pair) == 2:
					name = pair[0]
					size = pair[1]
					if system.search_sides_drinks(name, size) != None and int(qty) > 0:
						tempSD.append(system.search_sides_drinks(name, size))
			
			errorList = system.validate_inputs(tempMain,tempSD)
			if len(errorList) > 0:
				return render_template('home.html', ingredient_menu=system.get_ingredient_menu(), errorList = errorList, ingredient_qty=ingredient_qty, 
				sides_name=sides_name, sides_qty=sides_qty, drinks_qty=drinks_qty, drinks_name=drinks_name, desserts_name=desserts_name, desserts_qty=desserts_qty)
			else:
				for item in tempSD:
					sides_drinks.append(item)
				total_price = system.calc_net_price(mains, sides_drinks)
				
				for key in ingredient_qty.keys():
					ingredient_qty[key] = 0
				for key in sides_qty.keys():
					sides_qty[key] = 0
				for key in drinks_qty.keys():
					drinks_qty[key] = 0
				for key in desserts_qty.keys():
					desserts_qty[key] = 0
				
				return render_template('home.html', ingredient_menu=system.get_ingredient_menu(), ingredient_qty=ingredient_qty, sides_name=sides_name, sides_qty=sides_qty,
				drinks_name=drinks_name, drinks_qty=drinks_qty, desserts_name=desserts_name, desserts_qty=desserts_qty, mains=mains, sides_drinks=sides_drinks, total=total_price)
	
	return render_template('home.html')

''' Staff Page '''
@app.route('/staff', methods=["GET", "POST"])
def staff():
	if request.method == "POST":

		if 'order_list' in request.form:
			if len(system.get_current_order()) == 0:
				return render_template('staff.html', error='No current orders')
			return render_template('staff.html', orders=system.get_current_order())

		elif 'update_status' in request.form:
			system.update_status(int(request.form['update_status']))
			save_data(system)
			return render_template('staff.html', orders=system.get_current_order())

		elif 'all_stock' in request.form:
			if len(system.inventory.stock) == 0:
				return render_template('staff.html', error='No items in the system')
			return render_template('staff.html', ingredient_list=system.get_all_ingredients(), side_list=system.get_all_sides(), drink_list=system.get_all_drinks(), dessert_list=system.get_all_desserts())

		elif 'delete' in request.form:
			name = request.form['delete']
			size = request.form['size']
			system.remove_ingredient(name)
			system.remove_side_drink(name, size)
			save_data(system)
			return render_template('staff.html', ingredient_list=system.get_all_ingredients(), side_list=system.get_all_sides(), drink_list=system.get_all_drinks(), dessert_list=system.get_all_desserts())

		elif 'low_stock' in request.form:
			low_stock = system.inventory.find_low_stock()
			if len(low_stock) == 0:
				return render_template('staff.html', error='No low stock items')
			return render_template('staff.html', ingredient_low=system.inventory.find_low_stock_by_type('Ingredient'), side_low=system.inventory.find_low_stock_by_type('Side'), drink_low=system.inventory.find_low_stock_by_type('Drink'), dessert_low=system.inventory.find_low_stock_by_type('Dessert'))

		elif 'refill' in request.form or 'refill_all' in request.form:
			for name, qty in request.form.items():
				if system.inventory.search_stock(name) != None and qty != '':
					item = system.inventory.search_stock(name)
					system.inventory.update_stock(item, int(qty))
					save_data(system)
			if 'refill_all' in request.form:
				return render_template('staff.html', ingredient_list=system.get_all_ingredients(), side_list=system.get_all_sides(), drink_list=system.get_all_drinks(), dessert_list=system.get_all_desserts())
			return render_template('staff.html', ingredient_low=system.inventory.find_low_stock_by_type('Ingredient'), side_low=system.inventory.find_low_stock_by_type('Side'), drink_low=system.inventory.find_low_stock_by_type('Drink'), dessert_low=system.inventory.find_low_stock_by_type('Dessert'))

		elif 'refill_drink' in request.form or 'refill_drink_all' in request.form:
			for key, qty in request.form.items():
				if qty != '':
					pair = key.split('_',1)
					if len(pair) == 2 and int(qty) > 0:
						name = pair[0]
						size = pair[1]
						item = system.inventory.search_stock(name, size)
						system.inventory.update_stock(item, int(qty))
						save_data(system)
			if 'refill_drink_all' in request.form:
				return render_template('staff.html', ingredient_list=system.get_all_ingredients(), side_list=system.get_all_sides(), drink_list=system.get_all_drinks(), dessert_list=system.get_all_desserts())
			return render_template('staff.html', ingredient_low=system.inventory.find_low_stock_by_type('Ingredient'), side_low=system.inventory.find_low_stock_by_type('Side'), drink_low=system.inventory.find_low_stock_by_type('Drink'), dessert_low=system.inventory.find_low_stock_by_type('Dessert'))

		elif 'add_ingredient' in request.form:
			return render_template('staff.html', add_ingredient='add_ingredient')

		elif 'confirm' in request.form:
			errors = {}
			if request.form['name'] == '':
				errors['name'] = 'Name must not be empty'
			if request.form['price'] == '':
				errors['price'] = 'Price must not be empty'
			elif float(request.form['price']) == 0:
				errors['price'] = 'Price must be greater than 0'
			if request.form['calories'] == '':
				errors['calories'] = 'Calories must not be empty'
			elif int(request.form['calories']) == 0:
				errors['calories'] = 'Calories must be greater than 0'
			if request.form['decrement_qty'] == '':
				errors['decrement_qty'] = 'Decrement quantity must not be empty'
			elif int(request.form['decrement_qty']) == 0:
				errors['decrement_qty'] = 'Decrement quantity must be greater than 0'
			if request.form['stock_qty'] == '':
				errors['stock_qty'] = 'Stock quantity must not be empty'
			if len(errors) > 0:
				return render_template('staff.html', add_ingredient='add_ingredient', name=request.form['name'], price=request.form['price'], calories=request.form['calories'], decrement_qty=request.form['decrement_qty'], stock_qty=request.form['stock_qty'], errors=errors)

			name = request.form['name']
			price = float(request.form['price'])
			calories = int(request.form['calories'])
			decrement_qty = int(request.form['decrement_qty'])
			stock_qty = int(request.form['stock_qty'])

			ingredient = system.add_ingredient(name, price, calories, decrement_qty, stock_qty)
			if ingredient == None:
				return render_template('staff.html', error='Ingredient already exists')
			save_data(system)
			return render_template('staff.html', confirm='Ingredient added')

	return render_template('staff.html')
