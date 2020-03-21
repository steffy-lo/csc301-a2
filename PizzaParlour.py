from flask import Flask, jsonify, request, abort, make_response
import Pizza
import uuid
import datetime

app = Flask("Assignment 2")

orders = []
pickups = {}
pizza_parlour = Pizza.PizzaParlour()

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

@app.route('/new_pizza', methods=['POST'])
def new_pizza():
    req = request.get_json()
    # request body format example
    # {
    #     "name": "meat lovers",
    #     "price": 6,
    #     "ingredients": ["chicken", "beef"]
    # }
    if 'name' not in req or 'price' not in req or 'ingredients' not in req:
        abort(400)

    pizza_parlour.add_new_pizza(req["name"], req["price"], req["ingredients"])
    return jsonify(req)

@app.route('/set_pizza_price', methods=['PATCH'])
def set_pizza_price():
    req = request.get_json()
    # request body format example
    # {
    #     "name": "meat lovers",
    #     "price": 6,
    # }
    if 'name' not in req or 'price' not in req:
        abort(400)

    if req['name'] not in pizza_parlour.get_all_pizzas():
        abort(400)

    pizza_parlour.set_type_price(req["name"], req["price"])
    return jsonify({req["name"]: pizza_parlour.get_type_price(req["name"])})

@app.route('/set_size_price', methods=['PATCH'])
def set_size_price():
    req = request.get_json()
    # request body format example
    # {
    #     "size": "small",
    #     "price": 6,
    # }
    if 'size' not in req or 'price' not in req:
        abort(400)

    if req['size'] not in pizza_parlour.get_all_sizes():
        abort(400)

    pizza_parlour.set_size_price(req["size"], req["price"])
    return jsonify({req["size"]: pizza_parlour.get_size_price(req["size"])})

@app.route('/set_drink_price', methods=['PATCH'])
@app.route('/new_drink', methods=['POST'])
def set_drink_price():
    req = request.get_json()
    # request body format example
    # {
    #     "name": "fanta orange",
    #     "price": 2
    # }

    if 'name' not in req or 'price' not in req:
        abort(400)

    pizza_parlour.set_drink_price(req["name"], req["price"])
    return jsonify(req)

@app.route('/set_topping_price', methods=['PATCH'])
@app.route('/new_topping', methods=['POST'])
def set_topping_price():
    req = request.get_json()
    # request body format example
    # {
    #     "name": "cheese",
    #     "price": 2
    # }
    if 'name' not in req or 'price' not in req:
        abort(400)

    pizza_parlour.set_topping_price(req["name"], req["price"])
    return jsonify(req)

@app.route('/new_order', methods=['POST'])
def new_order():
    order_request = request.get_json()
    # request body format example
    # {
    #     "pizzas": [{"size": "small", "type": "pepperoni", "toppings": ["olives", "tomatoes"]}],
    #     "drinks": ["coke", "pepsi"]
    # }

    orderNum = uuid.uuid1().int >> 64
    order_response = {"orderNum": orderNum, "pizzas": [], "drinks": []}
    order = {"id": orderNum, "pizzas": [], "drinks": []}

    total = 0
    if 'pizzas' in order_request:
        pizza_orders = order_request['pizzas']
        for p in pizza_orders:
            # check for validity of order
            if p['size'] not in pizza_parlour.get_all_sizes() or p['type'] not in pizza_parlour.get_all_pizzas():
                abort(400)  # bad request
            o = pizza_parlour.create_pizza(p['size'], p['type'])
            order['pizzas'].append(o)
            order_response['pizzas'].append(o.itemID)
            for topping in p['toppings']:
                # check for validity of toppings
                if topping not in pizza_parlour.get_all_toppings():
                    abort(400)
                o.add_topping(topping)
            total += o.get_price(pizza_parlour)

    if 'drinks' in order_request:
        drink_orders = order_request['drinks']
        for d in drink_orders:
            if d not in pizza_parlour.get_all_drinks():
                abort(400)
            total += pizza_parlour.get_drink_price(d)
            order['drinks'].append(d)
            order_response['drinks'].append(d)

    order_response['price'] = total
    order['price'] = total
    orders.append(order)

    return jsonify(order_response)

@app.route('/update_order/<int:orderID>', methods=["PATCH"])
def update_order(orderID):

    find_order = [order for order in orders if order['id'] == orderID]
    if len(find_order) == 0:
        abort(404)  # invalid order id

    order = find_order[0]
    request_body = request.get_json()
    # request body format example
    # {
    #     "pizzas": [{"itemID": <str>, "size": "small", "type": "pepperoni", "add_toppings": ["mushrooms", "beef"], "del_toppings": []}],
    #     "drinks": {"add": ["water"], "remove": ["coke", "pepsi"]}
    # }
    found = False
    updated_price = order["price"]
    if 'pizzas' in request_body:
        pizzas = order["pizzas"]
        for toUpdate in request_body['pizzas']:
            for pizza in pizzas:
                print("pizza objectID:" + pizza.itemID)
                print("requested:" + toUpdate['itemID'])
                if pizza.itemID == toUpdate['itemID']:
                    found = True
                    if 'size' in toUpdate:
                        if toUpdate['size'] not in pizza_parlour.get_all_sizes():
                            print("invalid size")
                            abort(400)  # bad request
                        updated_price += \
                            pizza_parlour.get_size_price(toUpdate['size']) - pizza_parlour.get_size_price(pizza.size)
                        pizza.size = toUpdate['size']
                    if 'type' in toUpdate:
                        if toUpdate['type'] not in pizza_parlour.get_all_pizzas():
                            print("invalid type")
                            abort(400)
                        updated_price += \
                            pizza_parlour.get_type_price(toUpdate['type']) - pizza_parlour.get_type_price(pizza.type)
                        pizza.type = toUpdate['type']
                    if 'del_toppings' in toUpdate:
                        for topping in toUpdate['del_toppings']:
                            if topping not in pizza_parlour.get_all_toppings() or topping not in pizza.toppings:
                                print("invalid topping")
                                abort(400)
                            updated_price -= pizza_parlour.get_topping_price(topping)
                            pizza.remove_topping(topping)
                    if 'add_toppings' in toUpdate:
                        for topping in toUpdate['add_toppings']:
                            if topping not in pizza_parlour.get_all_toppings():
                                print("invalid topping")
                                abort(400)
                            updated_price += pizza_parlour.get_topping_price(topping)
                            pizza.add_topping(topping)
            if not found:
                print("invalid item ID")
                abort(400)  # itemID is invalid
            found = False

    if 'drinks' in request_body:
        if 'remove' in request_body['drinks']:
            for remove in request_body['drinks']['remove']:
                if remove not in pizza_parlour.get_all_drinks() or remove not in order['drinks']:
                    print("invalid drink")
                    abort(400)
                updated_price -= pizza_parlour.get_drink_price(remove)
                order['drinks'].remove(remove)
        if 'add' in request_body['drinks']:
            for add in request_body['drinks']['add']:
                if add not in pizza_parlour.get_all_drinks():
                    print("invalid drink")
                    abort(400)
                updated_price += pizza_parlour.get_drink_price(add)
                order['drinks'].append(add)

    updated_order = {
        "orderNum": orderID,
        "pizzas": [{"id": o.itemID,
                    "size": o.size,
                    "type": o.type,
                    "toppings": o.toppings} for o in order["pizzas"]],
        "drinks": order["drinks"],
        "price": updated_price
    }
    return jsonify(updated_order)

@app.route('/cancel_order/<int:orderID>', methods=["DELETE"])
def cancel_order(orderID):

    found_order = None
    for order in orders:
        if order['id'] == orderID:
            found_order = order
            break
    
    if not found_order:
        abort(404)

    res = {"orderID": found_order['id']}
    orders.remove(found_order)
    return jsonify(res)

@app.route('/pickup_order/<int:orderID>', methods=["POST"])
def pickup_order(orderID):
    found_order = None
    for order in orders:
        if order['id'] == orderID:
            found_order = order
            break

    if not found_order:
        abort(404)
    date = datetime.date.today()
    if str(date) in pickups:
        pickups[str(date)].append(found_order)
    else:
        pickups[str(date)] = [found_order]
    
    print (pickups)
    res = jsonify({str(date): found_order['id']})
    return res


@app.route('/display_menu', methods=["GET"])
def display_menu():

    all_sizes = pizza_parlour.get_all_sizes()
    all_toppings = pizza_parlour.get_all_toppings()
    all_types = pizza_parlour.get_all_pizzas()
    all_drinks = pizza_parlour.get_all_drinks()

    sizes = {}
    for size in all_sizes:
        sizes[size] = pizza_parlour.get_size_price(size)

    toppings = {}
    for topping in all_toppings:
        toppings[topping] = pizza_parlour.get_topping_price(topping)
    
    types = {}
    for pizza in all_types:
        types[pizza] = pizza_parlour.get_type_price(pizza)

    drinks = {}
    for drink in all_drinks:
        drinks[drink] = pizza_parlour.get_drink_price(drink)

    menu = {
        "size": sizes,
        "types": types,
        "toppings": toppings,
        "drinks": drinks
        }
    return jsonify(menu)


@app.route('/display_menu_item', methods=["GET"])
def display_menu_item():
    #{"pizza": {"size": "small"}}
    #{"pizza": {"size": "small", "type": "veggie", "toppings": ["mushroom"], "drink": "coke"}}
    # {"drink": "pepsi"}

    #either request a pizza or a drink
    item = request.get_json()

    price = 0
    sizes = pizza_parlour.get_all_sizes()
    toppings = pizza_parlour.get_all_toppings()
    types = pizza_parlour.get_all_pizzas()

    for category, value in item.items():
        if category == "drink":
            if value in pizza_parlour.get_all_drinks():
                price += pizza_parlour.get_drink_price(value)
            else:
                abort(400)
        elif category == "pizza":
            for key, stuff in value.items():
                if key == "size":
                    if stuff not in sizes:
                        print("invalid size")
                        abort(400)
                    price += pizza_parlour.get_size_price(stuff)
                elif key == "type":
                    if stuff not in types:
                        print("invalid type")
                        abort(400)
                    price += pizza_parlour.get_type_price(stuff)
                elif key == "toppings":
                    for topping in stuff:
                        if topping not in toppings:
                            print("invalid topping")
                            abort(400)
                        price += pizza_parlour.get_topping_price(topping)
                else:
                    print("invalid key")
                    abort(400)
        else:
            print("invalid menu item")
            abort(400)

    item["price"] = price
    return jsonify(item)

if __name__ == "__main__":
    app.run()
