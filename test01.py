from restaurant_system import RestaurantSystem
from ingredient import Ingredient
from order import Order
from main import Main, Burger, Wrap
from side_drink import SideDrink
from error import OrderError, check_order_error
from inventory import Inventory

import pytest

'''
	Test US1, US2, US3, US4, US5, US6
	regarding "Placing Order", "Checking Order Status"
'''

@pytest.fixture
def gourmet_fixture():
    system = RestaurantSystem()
	
    bun_list = ['Bun', 'Sandwich']
    patty_list = ['Chicken Patty', 'Vegetarian Patty', 'Beef Patty']
    ingredient_list = ['Tomato', 'Lettuce', 'Tomato Sauce', 'Chili Sauce', 'Mayonnaise Sauce', 'Cheddar Cheese', 'Sweet Cheese']
    
    for name in bun_list:
        system.ingredients.append(get_ingredient_by_name(name))
        system.inventory.update_stock(get_ingredient_by_name(name),500)
    for name in patty_list:
        system.ingredients.append(get_ingredient_by_name(name))
        system.inventory.update_stock(get_ingredient_by_name(name),1000)
    for name in ingredient_list:
        system.ingredients.append(get_ingredient_by_name(name))
        system.inventory.update_stock(get_ingredient_by_name(name),800)
    
    side_list = ['Nugget', 'Chips', 'Salad', 'Rice', 'Grilled Corn']
    contained_list = ['Water', 'Coca Cola', 'Fanta', 'Sprite', 'Sunkist']
    juice_list = ['Orange Juice', 'Watermelon', 'Pineapple', 'Apple']
    
    for name in side_list:
        system.sides_drinks.append(get_side_drink_by_name(name,"Small"))
        system.sides_drinks.append(get_side_drink_by_name(name,"Medium"))
        system.sides_drinks.append(get_side_drink_by_name(name,"Large"))
        system.inventory.update_stock(get_side_drink_by_name(name,"Small"),2000)
    for name in contained_list:
        system.sides_drinks.append(get_side_drink_by_name(name,"Can"))
        system.sides_drinks.append(get_side_drink_by_name(name,"Bottle"))
        system.inventory.update_stock(get_side_drink_by_name(name,"Can"),200)
        system.inventory.update_stock(get_side_drink_by_name(name,"Bottle"),200)
    for name in juice_list:
        system.sides_drinks.append(get_side_drink_by_name(name,"Small"))
        system.sides_drinks.append(get_side_drink_by_name(name,"Medium"))
        system.inventory.update_stock(get_side_drink_by_name(name,"Small"),200)
        system.inventory.update_stock(get_side_drink_by_name(name,"Medium"),200)
   
    return system

def test_view_menu(gourmet_fixture):
	print("Test viewing menu options")
	
	assert len(gourmet_fixture.inventory.find_in_stock()) == 31
	gourmet_fixture.inventory.update_stock(Ingredient('Onion', 2, 300, 1),0)
	assert len(gourmet_fixture.inventory.find_in_stock()) == 31
	
	in_stock = gourmet_fixture.inventory.find_in_stock()
	for item in in_stock:
		assert item.name != None and item.price != None and item.calories != None

def test_make_single_order(gourmet_fixture):
    print("Testing make single order")

    mainType = "Burger"
    ingredients = {get_ingredient_by_name("Bun"):2, get_ingredient_by_name("Chicken Patty"):1, get_ingredient_by_name("Tomato"):1,
	get_ingredient_by_name("Lettuce"):1, get_ingredient_by_name("Cheddar Cheese"):2, get_ingredient_by_name("Chili Sauce"):1}
    sides_drinks = []
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Fanta', 'Bottle'))
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Chips', 'Large'))

    mains = []
    mains.append(gourmet_fixture.create_main(mainType, ingredients))

    price = gourmet_fixture.calc_net_price(mains, sides_drinks)
    
    assert price == 17.5

    id = gourmet_fixture.make_order(mains, sides_drinks)
    assert id == 1
    assert len(gourmet_fixture.orders) == 1
    assert gourmet_fixture.inventory.find_ingredient_quantity("Tomato") == 799
    assert gourmet_fixture.inventory.find_ingredient_quantity("Bun") == 498
    assert gourmet_fixture.inventory.find_drink_quantity("Fanta", "Bottle") == 199
    assert gourmet_fixture.inventory.find_ingredient_quantity("Chips") == 1825

def test_make_multiple_order(gourmet_fixture):
    print("Testing make multiple orders")
    mainType = "Burger"
	
    ingredients = {get_ingredient_by_name("Bun"):2, get_ingredient_by_name("Chicken Patty"):1, get_ingredient_by_name("Tomato"):1,
	get_ingredient_by_name("Lettuce"):1, get_ingredient_by_name("Cheddar Cheese"):2, get_ingredient_by_name("Chili Sauce"):1}
    sides_drinks = []
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Fanta', 'Bottle'))
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Chips', 'Large'))

    mains = []
    mains.append(gourmet_fixture.create_main(mainType, ingredients))

    price = gourmet_fixture.calc_net_price(mains, sides_drinks)
    assert price == 17.5

    id = gourmet_fixture.make_order(mains, sides_drinks)
    assert id == 1
    assert len(gourmet_fixture.orders) == 1
    assert gourmet_fixture.inventory.find_ingredient_quantity("Tomato") == 799
    assert gourmet_fixture.inventory.find_ingredient_quantity("Bun") == 498
    assert gourmet_fixture.inventory.find_drink_quantity("Fanta", "Bottle") == 199

    mainType = "Burger"
    ingredients = {get_ingredient_by_name("Bun"):3, get_ingredient_by_name("Chicken Patty"):4, get_ingredient_by_name("Tomato"):2,
    get_ingredient_by_name("Lettuce"):3, get_ingredient_by_name("Cheddar Cheese"):2, get_ingredient_by_name("Chili Sauce"):1, get_ingredient_by_name("Sweet Cheese"):1}
    sides_drinks = []
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Apple', 'Small'))
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Chips', 'Small'))

    mains = []
    mains.append(gourmet_fixture.create_main(mainType, ingredients))

    price = gourmet_fixture.calc_net_price(mains, sides_drinks)

    assert price == 36.5
    id = gourmet_fixture.make_order(mains, sides_drinks)
    assert id == 2
    assert len(gourmet_fixture.orders) == 2
    assert gourmet_fixture.inventory.find_ingredient_quantity("Tomato") == 797
    assert gourmet_fixture.inventory.find_ingredient_quantity("Bun") == 495
    assert gourmet_fixture.inventory.find_drink_quantity("Fanta", "Bottle") == 199
    assert gourmet_fixture.inventory.find_ingredient_quantity("Chips") == 1750

def test_single_order_with_multiple_burger(gourmet_fixture):
    print("Testing make single order with multiple burgers")

    mains = []

    mainType = "Burger"
    ingredients = {get_ingredient_by_name("Bun"):2, get_ingredient_by_name("Chicken Patty"):1, get_ingredient_by_name("Tomato"):1,
	get_ingredient_by_name("Lettuce"):1, get_ingredient_by_name("Cheddar Cheese"):2, get_ingredient_by_name("Chili Sauce"):1}
    sides_drinks = []
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Fanta', 'Bottle'))
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Chips', 'Large'))

    mains.append(gourmet_fixture.create_main(mainType, ingredients))
    price = gourmet_fixture.calc_net_price(mains, sides_drinks)
    assert price == 17.5

    mainType = "Burger"
    ingredients = {get_ingredient_by_name("Bun"):3, get_ingredient_by_name("Chicken Patty"):4, get_ingredient_by_name("Tomato"):2,
    get_ingredient_by_name("Lettuce"):3, get_ingredient_by_name("Cheddar Cheese"):2, get_ingredient_by_name("Chili Sauce"):1, get_ingredient_by_name("Sweet Cheese"):1}
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Apple', 'Small'))
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Chips', 'Small'))

    mains.append(gourmet_fixture.create_main(mainType, ingredients))
    price = gourmet_fixture.calc_net_price(mains,sides_drinks)
    assert price == 54

    id = gourmet_fixture.make_order(mains, sides_drinks)
    assert id == 1
    assert len(gourmet_fixture.orders) == 1
    assert gourmet_fixture.inventory.find_ingredient_quantity("Tomato") == 797
    assert gourmet_fixture.inventory.find_ingredient_quantity("Bun") == 495
    assert gourmet_fixture.inventory.find_drink_quantity("Fanta", "Bottle") == 199
    assert gourmet_fixture.inventory.find_ingredient_quantity("Chips") == 1750

def test_order_too_many_patties(gourmet_fixture):
    print("Testing invalid input with too many patties")

    mainType = "Burger"
    ingredients = {get_ingredient_by_name("Bun"):2, get_ingredient_by_name("Chicken Patty"):7, get_ingredient_by_name("Tomato"):1,
        get_ingredient_by_name("Lettuce"):1, get_ingredient_by_name("Cheddar Cheese"):2, get_ingredient_by_name("Chili Sauce"):1}
    sides_drinks = []

    mains = []
    mains.append(gourmet_fixture.create_main(mainType, ingredients))

    with pytest.raises(OrderError) as info:
        _ = gourmet_fixture.calc_net_price(mains, sides_drinks)
    assert "Sorry, please enter number of Chicken Patty between 1 to 2." in str(info.value)

def test_order_not_enough_stock(gourmet_fixture):
    print("Testing invalid input with unavailable ingredient")

    gourmet_fixture.inventory.update_stock(get_ingredient_by_name("Mayonnaise Sauce"),-799)
    assert gourmet_fixture.inventory.find_ingredient_quantity("Mayonnaise Sauce") == 1
    mainType = "Burger"
    ingredients = {get_ingredient_by_name("Bun"):2, get_ingredient_by_name("Chicken Patty"):7, get_ingredient_by_name("Tomato"):1,
        get_ingredient_by_name("Lettuce"):1, get_ingredient_by_name("Cheddar Cheese"):2, get_ingredient_by_name("Mayonnaise Sauce"):2}
    sides_drinks = []

    mains = []
    mains.append(gourmet_fixture.create_main(mainType, ingredients))
    with pytest.raises(OrderError) as info:
        _ = gourmet_fixture.calc_net_price(mains, sides_drinks)
    assert "Sorry, not enough stock for Mayonnaise Sauce" in str(info.value)

def test_order_not_enough_side(gourmet_fixture):
    print("Testing invalid input with unavailable side")

    gourmet_fixture.inventory.update_stock(get_side_drink_by_name("Chips", "Large"),-1925)
    assert gourmet_fixture.inventory.find_ingredient_quantity("Chips") == 75
    mainType = "Burger"
    ingredients = {get_ingredient_by_name("Bun"):2, get_ingredient_by_name("Chicken Patty"):1, get_ingredient_by_name("Tomato"):1,
        get_ingredient_by_name("Lettuce"):1, get_ingredient_by_name("Cheddar Cheese"):2, get_ingredient_by_name("Mayonnaise Sauce"):2}
    sides_drinks = []
    sides_drinks.append(gourmet_fixture.search_sides_drinks('Chips', 'Large'))
    mains = []
    mains.append(gourmet_fixture.create_main(mainType,ingredients))

    with pytest.raises(OrderError) as info:
        _ = gourmet_fixture.calc_net_price(mains, sides_drinks)
    assert "Sorry, not enough stock for Chips" in str(info.value)

def test_order_too_many_lettuce(gourmet_fixture):
    print("Testing invalid input with too many lettuce")

    mainType = "Burger"
    ingredients = {get_ingredient_by_name("Bun"):2, get_ingredient_by_name("Chicken Patty"):1, get_ingredient_by_name("Tomato"):1,
        get_ingredient_by_name("Lettuce"):11, get_ingredient_by_name("Cheddar Cheese"):2, get_ingredient_by_name("Mayonnaise Sauce"):2}
    sides_drinks = []
    mains = []
    mains.append(gourmet_fixture.create_main(mainType, ingredients))
    with pytest.raises(OrderError) as info:
        _ = gourmet_fixture.calc_net_price(mains, sides_drinks)
    assert "Sorry, please enter Lettuce amount between 0 and 10." in str(info.value)

def test_check_valid_id(gourmet_fixture):
	print("Test checking an order status")
	
	mains1 = []
	ingredients1 = {}
	ingredients1.update({gourmet_fixture.search_ingredient('Bun'):2})
	ingredients1.update({gourmet_fixture.search_ingredient('Chicken Patty'):2})
	ingredients1.update({gourmet_fixture.search_ingredient('Tomato'):1})
	ingredients1.update({gourmet_fixture.search_ingredient('Lettuce'):1})
	ingredients1.update({gourmet_fixture.search_ingredient('Tomato Sauce'):1})
	ingredients1.update({gourmet_fixture.search_ingredient('Cheddar Cheese'):1})
	mains1.append(gourmet_fixture.create_main('Burger', ingredients1))
	
	mains2 = []
	ingredients2 = {}
	ingredients2.update({gourmet_fixture.search_ingredient('Sandwich'):1})
	ingredients2.update({gourmet_fixture.search_ingredient('Beef Patty'):2})
	ingredients2.update({gourmet_fixture.search_ingredient('Tomato'):2})
	ingredients2.update({gourmet_fixture.search_ingredient('Lettuce'):1})
	ingredients2.update({gourmet_fixture.search_ingredient('Chili Sauce'):1})
	ingredients2.update({gourmet_fixture.search_ingredient('Sweet Cheese'):2})
	mains2.append(gourmet_fixture.create_main('Wrap', ingredients2))
	
	sides_drinks = []
	sides_drinks.append(gourmet_fixture.search_sides_drinks('Fanta', 'Bottle'))
	sides_drinks.append(gourmet_fixture.search_sides_drinks('Chips', 'Large'))
	
	gourmet_fixture.make_order(mains1, sides_drinks)
	assert len(gourmet_fixture.orders) == 1
	assert gourmet_fixture.check_order_status(1) == 'Queueing'
	gourmet_fixture.make_order(mains2, sides_drinks)
	assert len(gourmet_fixture.orders) == 2
	assert gourmet_fixture.check_order_status(2) == 'Queueing'
	gourmet_fixture.update_status(2)
	assert gourmet_fixture.check_order_status(2) == 'Preparing'
	gourmet_fixture.update_status(2)
	assert gourmet_fixture.check_order_status(2) == 'Ready to collect'
	gourmet_fixture.update_status(2)
	assert gourmet_fixture.check_order_status(2) == 'Collected'
	assert gourmet_fixture.check_order_status(1) == 'Queueing'

def test_check_invalid_id(gourmet_fixture):
	print("Test checking an invalid ID")
	
	mains1 = []
	ingredients1 = {}
	ingredients1.update({gourmet_fixture.search_ingredient('Bun'):2})
	ingredients1.update({gourmet_fixture.search_ingredient('Chicken Patty'):2})
	ingredients1.update({gourmet_fixture.search_ingredient('Tomato'):1})
	ingredients1.update({gourmet_fixture.search_ingredient('Lettuce'):1})
	ingredients1.update({gourmet_fixture.search_ingredient('Tomato Sauce'):1})
	ingredients1.update({gourmet_fixture.search_ingredient('Cheddar Cheese'):1})
	mains1.append(gourmet_fixture.create_main('Burger', ingredients1))
	
	sides_drinks = []
	sides_drinks.append(gourmet_fixture.search_sides_drinks('Fanta', 'Bottle'))
	sides_drinks.append(gourmet_fixture.search_sides_drinks('Chips', 'Large'))
	
	gourmet_fixture.make_order(mains1, sides_drinks)
	assert gourmet_fixture.check_order_status(1) == 'Queueing'
	assert gourmet_fixture.check_order_status(None) == 'Type in a valid order ID'
	assert gourmet_fixture.check_order_status(3) == 'Your order no longer exists'
	assert gourmet_fixture.check_order_status('ab123') == 'Your order no longer exists'

'''
	Helper Functions
'''

def get_ingredient_by_name(name):
    if name in ("Bun", "Sandwich"):
        return Ingredient(name,2,300,1)
    elif name in ('Chicken Patty', 'Vegetarian Patty', 'Beef Patty'):
        return Ingredient(name,5,600,1)
    else:
        return Ingredient(name,0.5,50,1)

def get_side_drink_by_name(name, size):
    if name in ('Nugget', 'Chips', 'Salad', 'Rice', 'Grilled Corn'):
        if size == "Small":
            return SideDrink(name,"Side",size,2,200,75)
        elif size == "Medium":
            return SideDrink(name,"Side",size,2.5,300,125)
        else:
            return SideDrink(name,"Side",size,3,400,175)
    elif name in ('Water', 'Coca Cola', 'Fanta', 'Sprite', 'Sunkist'):
        if size == "Can":
            return SideDrink(name,"Drink",size,2,100,1)
        else:
            return SideDrink(name,"Drink",size,3,200,1)
    else:
        if size == "Small":
            return SideDrink(name,"Drink",size,4,150,250)
        else:
            return SideDrink(name,"Drink",size,5,200,450)
    
    return None
