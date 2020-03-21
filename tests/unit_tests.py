from PizzaParlour import app
import uuid
import PizzaParlour, Pizza
import json

pizza_parlour = Pizza.PizzaParlour()

def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'

def test_new_valid_order():
    mock_data = {
        "pizzas": [
            {"size": "small", "type": "pepperoni", "toppings": ["olives", "tomatoes"]},
            {"size": "small", "type": "margherita", "toppings": ["olives", "tomatoes"]},
            {"size": "small", "type": "vegetarian", "toppings": ["olives", "tomatoes"]},
            {"size": "small", "type": "neapolitan", "toppings": ["olives", "tomatoes"]}
                   ],
        "drinks": ["coke", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 200

def test_add_new_pizza_type():
    mock_data = {
        "name": "meat lovers",
        "price": 6,
        "ingredients": ["chicken", "beef"]
    }
    response = app.test_client().post('/new_pizza', json=mock_data)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["name"] in _read_pizza_data()["types"]

def test_set_pizza_price():
    mock_data = {
        "name": "pepperoni",
        "price": 4
    }
    response = app.test_client().patch('/set_pizza_price', json=mock_data)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["pepperoni"] == _read_pizza_data()["types"]["pepperoni"]

def test_invalid_set_pizza_price():
    mock_data = {
        "price": 4
    }
    response = app.test_client().patch('/set_pizza_price', json=mock_data)
    assert response.status_code == 400

def test_set_invalid_pizza_price():
    mock_data = {
        "name": "spicy",
        "price": 4
    }
    response = app.test_client().patch('/set_pizza_price', json=mock_data)
    assert response.status_code == 400

def test_invalid_add_new_pizza_type():
    mock_data = {
        "name": "meat lovers",
        "price": 6
    }
    response = app.test_client().post('/new_pizza', json=mock_data)
    assert response.status_code == 400

def test_set_size_price():
    mock_data = {
        "size": "large",
        "price": 4
    }
    response = app.test_client().patch('/set_size_price', json=mock_data)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["large"] == _read_pizza_data()["sizes"]["large"]

def test_invalid_set_size_price():
    mock_data = {
        "price": 4
    }
    response = app.test_client().patch('/set_size_price', json=mock_data)
    assert response.status_code == 400

def test_set_invalid_size_price():
    mock_data = {
        "size": "tall",
        "price": 4
    }
    response = app.test_client().patch('/set_size_price', json=mock_data)
    assert response.status_code == 400

def test_add_new_drink():
    mock_data = {
            "name": "fanta orange",
            "price": 2
        }
    response = app.test_client().post('/new_drink', json=mock_data)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["name"] in _read_drink_data()

def test_invalid_add_new_drink():
    mock_data = {
            "name": "fanta orange"
        }
    response = app.test_client().post('/new_drink', json=mock_data)
    assert response.status_code == 400

def test_add_new_topping():
    mock_data = {
        "name": "cheddar",
        "price": 2
    }
    response = app.test_client().post('/new_topping', json=mock_data)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["name"] in _read_pizza_data()["toppings"]

def test_invalid_add_new_topping():
    mock_data = {
        "name": "cheddar"
    }
    response = app.test_client().post('/new_topping', json=mock_data)
    assert response.status_code == 400

def test_invalid_size():
    # invalid size
    mock_data = {
        "pizzas": [{"size": "tall", "type": "pepperoni", "toppings": ["olives", "tomatoes"]}],
        "drinks": ["coke", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 400


def test_invalid_type():
    # invalid type
    mock_data = {
        "pizzas": [{"size": "tall", "type": "meat lover", "toppings": ["olives", "tomatoes"]}],
        "drinks": ["coke", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 400


def test_invalid_topping():
    # invalid topping
    mock_data = {
        "pizzas": [{"size": "small", "type": "pepperoni", "toppings": ["cheese", "tomatoes"]}],
        "drinks": ["coke", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 400


def test_invalid_drink():
    # invalid drink
    mock_data = {
        "pizzas": [{"size": "small", "type": "pepperoni", "toppings": ["olives", "tomatoes"]}],
        "drinks": ["7up", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 400

### NEED TO FIX PRICE TEST FOR THIS METHOD AND ANY OTHER METHODS WITH PRICE ASSERTIONS
def test_valid_update_order():
    order = _create_mock_order()
    o = pizza_parlour.create_pizza("small", "pepperoni")
    o.add_topping("tomatoes")
    test_itemID = o.itemID
    order['pizzas'].append(o)
    order['drinks'].append("coke")
    order['drinks'].append("pepsi")
    order['price'] = o.get_price(pizza_parlour) + \
                     pizza_parlour.get_drink_price("coke") + \
                     pizza_parlour.get_drink_price("pepsi")
    PizzaParlour.orders.append(order)

    mock_data = {
        "pizzas": [{"itemID": test_itemID,
                    "size": "medium",
                    "type": "pepperoni",
                    "add_toppings": ["mushrooms", "beef"], "del_toppings": ["tomatoes"]}],
        "drinks": {"add": ["water", "juice"], "remove": ["coke", "pepsi"]}
        }
    response = app.test_client().patch('/update_order/' + str(order["id"]), json=mock_data)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["orderNum"] == order["id"]
    assert json_data["drinks"] == ["water", "juice"]
    new_pizza = pizza_parlour.create_pizza("medium", "pepperoni")
    new_pizza.add_topping("mushrooms")
    new_pizza.add_topping("beef")
    updated_price = new_pizza.get_price(pizza_parlour)
    updated_price += pizza_parlour.get_drink_price("water")
    updated_price += pizza_parlour.get_drink_price("juice")
    assert json_data["price"] == updated_price

def test_invalid_orderId_update_order():
    order = _create_mock_order()
    o = pizza_parlour.create_pizza("small", "pepperoni")
    o.add_topping("tomatoes")
    test_itemID = o.itemID
    order['pizzas'].append(o)
    order['price'] = o.get_price(pizza_parlour)
    PizzaParlour.orders.append(order)

    mock_data = {
        "pizzas": [{"itemID": test_itemID,
                    "size": "tall",
                    "type": "pepperoni",
                    "add_toppings": ["mushrooms", "beef"], "del_toppings": ["tomatoes"]}],
        "drinks": {"add": ["water", "juice"]}
        }
    response = app.test_client().patch('/update_order/' + str(1234), json=mock_data)
    assert response.status_code == 404

def test_invalid_size_update_order():
    order = _create_mock_order()
    o = pizza_parlour.create_pizza("small", "pepperoni")
    o.add_topping("tomatoes")
    test_itemID = o.itemID
    order['pizzas'].append(o)
    order['price'] = o.get_price(pizza_parlour)
    PizzaParlour.orders.append(order)

    mock_data = {
        "pizzas": [{"itemID": test_itemID,
                    "size": "tall",
                    "type": "pepperoni",
                    "add_toppings": ["mushrooms", "beef"], "del_toppings": ["tomatoes"]}],
        "drinks": {"add": ["water", "juice"]}
        }
    response = app.test_client().patch('/update_order/' + str(order["id"]), json=mock_data)
    assert response.status_code == 400

def test_invalid_type_update_order():
    order = _create_mock_order()
    o = pizza_parlour.create_pizza("small", "pepperoni")
    o.add_topping("tomatoes")
    test_itemID = o.itemID
    order['pizzas'].append(o)
    order['price'] = o.get_price(pizza_parlour)
    PizzaParlour.orders.append(order)

    mock_data = {
        "pizzas": [{"itemID": test_itemID,
                    "size": "medium",
                    "type": "meat lover"}]
        }
    response = app.test_client().patch('/update_order/' + str(order["id"]), json=mock_data)
    assert response.status_code == 400

def test_invalid_add_topping_update_order():
    order = _create_mock_order()
    o = pizza_parlour.create_pizza("small", "pepperoni")
    o.add_topping("tomatoes")
    test_itemID = o.itemID
    order['pizzas'].append(o)
    order['price'] = o.get_price(pizza_parlour)
    PizzaParlour.orders.append(order)

    mock_data = {
        "pizzas": [{"itemID": test_itemID,
                    "size": "medium",
                    "type": "pepperoni",
                    "add_toppings": ["mushrooms", "green pepper"], "del_toppings": ["tomatoes"]}],
        "drinks": {"add": ["water", "juice"]}
    }
    response = app.test_client().patch('/update_order/' + str(order["id"]), json=mock_data)
    assert response.status_code == 400

def test_invalid_del_topping_update_order():
    order = _create_mock_order()
    o = pizza_parlour.create_pizza("small", "pepperoni")
    o.add_topping("tomatoes")
    test_itemID = o.itemID
    order['pizzas'].append(o)
    order['price'] = o.get_price(pizza_parlour)
    PizzaParlour.orders.append(order)

    mock_data = {
        "pizzas": [{"itemID": test_itemID,
                    "size": "medium",
                    "type": "pepperoni",
                    "add_toppings": ["mushrooms", "beef"], "del_toppings": ["chicken"]}],
        "drinks": {"add": ["water", "juice"]}
    }
    response = app.test_client().patch('/update_order/' + str(order["id"]), json=mock_data)
    assert response.status_code == 400

def test_invalid_itemId_update_order():
    order = _create_mock_order()
    o = pizza_parlour.create_pizza("small", "pepperoni")
    o.add_topping("tomatoes")
    order['pizzas'].append(o)
    order['price'] = o.get_price(pizza_parlour)
    PizzaParlour.orders.append(order)

    mock_data = {
        "pizzas": [{"itemID": "invalid",
                    "size": "medium",
                    "type": "pepperoni",
                    "add_toppings": ["mushrooms", "beef"], "del_toppings": ["tomatoes"]}],
        "drinks": {"add": ["water", "juice"]}
    }
    response = app.test_client().patch('/update_order/' + str(order["id"]), json=mock_data)
    assert response.status_code == 400

def test_invalid_add_drink_update_order():
    order = _create_mock_order()
    o = pizza_parlour.create_pizza("small", "pepperoni")
    test_itemID = o.itemID
    o.add_topping("tomatoes")
    order['pizzas'].append(o)
    order['price'] = o.get_price(pizza_parlour)
    PizzaParlour.orders.append(order)

    mock_data = {
        "pizzas": [{"itemID": test_itemID,
                    "size": "medium",
                    "type": "pepperoni",
                    "add_toppings": ["mushrooms", "beef"], "del_toppings": ["tomatoes"]}],
        "drinks": {"add": ["pop", "juice"]}
    }
    response = app.test_client().patch('/update_order/' + str(order["id"]), json=mock_data)
    assert response.status_code == 400

def test_invalid_del_drink_update_order():
    order = _create_mock_order()
    o = pizza_parlour.create_pizza("small", "pepperoni")
    test_itemID = o.itemID
    o.add_topping("tomatoes")
    order['pizzas'].append(o)
    order['price'] = o.get_price(pizza_parlour)
    order['drinks'].append("coke")
    PizzaParlour.orders.append(order)

    mock_data = {
        "pizzas": [{"itemID": test_itemID,
                    "size": "medium",
                    "type": "pepperoni",
                    "add_toppings": ["mushrooms", "beef"], "del_toppings": ["tomatoes"]}],
        "drinks": {"remove": ["water"]}
    }
    response = app.test_client().patch('/update_order/' + str(order["id"]), json=mock_data)
    assert response.status_code == 400

def test_del_valid_order():
    order = _create_mock_order()
    order["drinks"].append("water")
    order_id = order["id"]
    PizzaParlour.orders.append(order)

    response = app.test_client().delete('/cancel_order/' + str(order_id))
    assert response.status_code == 200

def test_del_invalid_order():

    response = app.test_client().delete('/cancel_order/' + str(1234))
    assert response.status_code == 404

def test_get_full_menu():
    response = app.test_client().get('/display_menu')
    assert response.status_code == 200

def test_get_menu_item_valid_drink():
    req = {"drink": "pepsi"}
    response = app.test_client().get('/display_menu_item', json=req)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["price"] == _read_drink_data()["pepsi"]
    
def test_get_menu_item_invalid_drink():
    req = {"drink": "pizza"}
    response = app.test_client().get('/display_menu_item', json=req)
    assert response.status_code == 400

def test_get_menu_item_valid_pizza():
    req = {
        "pizza": {
            "size": "small", 
            "type": "pepperoni", 
            "toppings": ["chicken", "mushrooms"]
            }
        }
    response = app.test_client().get('/display_menu_item', json=req)
    json_data = response.get_json()

    assert response.status_code == 200
    pizza_menu = _read_pizza_data()
    sizes = pizza_menu["sizes"]
    types = pizza_menu["types"]
    toppings = pizza_menu["toppings"]
    assert json_data["price"] == sizes["small"] + types["pepperoni"] + toppings["chicken"] + toppings["mushrooms"]

def test_get_menu_item_invalid_pizza_size():
    req = {
        "pizza": {
            "size": "TALL", 
            "type": "pepperoni", 
            "toppings": ["chicken", "mushrooms"]
            }
        }
    response = app.test_client().get('display_menu_item', json=req)
    assert response.status_code == 400

def test_menu_item_invalid_pizza_type():
    req = {
        "pizza": {
            "size": "small", 
            "type": "cheeto", 
            "toppings": ["chicken", "mushrooms"]
            }
        }
    response = app.test_client().get('display_menu_item', json=req)
    assert response.status_code == 400

def test_menu_item_invalid_toppings():
    req = {
        "pizza": {
            "size": "small", 
            "type": "pepperoni", 
            "toppings": ["chick", "fajita"]
            }
        }
    response = app.test_client().get('display_menu_item', json=req)
    assert response.status_code == 400

def test_invalid_menu_item_choice():
    req = {
        "dessert": {
            "size": "tall"
            }
        }
    response = app.test_client().get('display_menu_item', json=req)
    assert response.status_code == 400

def test_invalid_pizza_attribute():
    req = {
        "pizza": {
            "crust": "small",
            "type": "pepperoni",
            "toppings": ["chicken", "mushrooms"]
        }
    }
    response = app.test_client().get('display_menu_item', json=req)
    assert response.status_code == 400

#=================================== HELPER METHODS ==================================================================


def _create_mock_order():
    order_num = uuid.uuid1().int >> 64
    return {"id": order_num, "pizzas": [], "drinks": []}


def _read_pizza_data():
    pizza_file = open("pizza.json", "r")
    pizza_menu = json.load(pizza_file)
    pizza_file.close()
    return pizza_menu


def _read_drink_data():
    drinks_file = open("drink.json", "r")
    drinks_menu = json.load(drinks_file)
    drinks_file.close()
    return drinks_menu
