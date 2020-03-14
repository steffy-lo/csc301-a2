from flask import Flask, jsonify, request, abort
import Pizza
import uuid

app = Flask("Assignment 2")

orders = []
pizza_factory = Pizza.PizzaFactory()
drinks_menu = {'coke': 2,
              'diet coke': 2,
              'coke zero': 2,
              'pepsi': 2,
              'diet pepsi': 2,
              'dr. pepper': 3.5,
              'water': 1,
              'juice': 4}

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

@app.route('/new_order', methods=['POST'])
def new_order():
    # request.args.get
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
            if p['size'] not in pizza_factory.get_all_sizes() or p['type'] not in pizza_factory.get_all_pizzas():
                abort(400)  # bad request
            o = pizza_factory.create_pizza(p['size'], p['type'])
            order['pizzas'].append(o)
            order_response['pizzas'].append(o.itemID)
            for topping in p['toppings']:
                # check for validity of toppings
                if topping not in pizza_factory.get_all_toppings():
                    abort(400)
                o.add_topping(topping)
            total += o.get_price(pizza_factory)

    if 'drinks' in order_request:
        drink_orders = order_request['drinks']
        for d in drink_orders:
            if d not in drinks_menu:
                abort(400)
            total += drinks_menu[d]
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
    #     "pizzas": [{"itemID": "4a2f4998-7670-4dd5-a768-fe7f31d9158d", "size": "small", "type": "pepperoni", "add_toppings": ["mushrooms", "beef"], "del_toppings": []}],
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
                        if toUpdate['size'] not in pizza_factory.get_all_sizes():
                            print("invalid size")
                            abort(400)  # bad request
                        updated_price += \
                            pizza_factory.get_size_price(toUpdate['size']) - pizza_factory.get_size_price(pizza.size)
                        pizza.size = toUpdate['size']
                    if 'type' in toUpdate:
                        if toUpdate['type'] not in pizza_factory.get_all_pizzas():
                            print("invalid type")
                            abort(400)
                        updated_price += \
                            pizza_factory.get_type_price(toUpdate['type']) - pizza_factory.get_type_price(pizza.type)
                        pizza.type = toUpdate['type']
                    if 'del_toppings' in toUpdate:
                        for topping in toUpdate['del_toppings']:
                            if topping not in pizza_factory.get_all_toppings() or topping not in pizza.toppings:
                                print("invalid topping")
                                abort(400)
                            updated_price -= pizza_factory.get_topping_price(topping)
                            pizza.remove_topping(topping)
                    if 'add_toppings' in toUpdate:
                        for topping in toUpdate['add_toppings']:
                            if topping not in pizza_factory.get_all_toppings():
                                print("invalid topping")
                                abort(400)
                            updated_price += pizza_factory.get_topping_price(topping)
                            pizza.add_topping(topping)
            if not found:
                print("invalid item ID")
                abort(400)  # itemID is invalid
            found = False

    if 'drinks' in request_body:
        if 'remove' in request_body['drinks']:
            for remove in request_body['drinks']['remove']:
                if remove not in drinks_menu or remove not in order['drinks']:
                    print("invalid drink")
                    abort(400)
                updated_price -= drinks_menu[remove]
                order['drinks'].remove(remove)
        if 'add' in request_body['drinks']:
            for add in request_body['drinks']['add']:
                if add not in drinks_menu:
                    print("invalid drink")
                    abort(400)
                updated_price += drinks_menu[add]
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

# @app.route('/display_menu/<int:choice>', methods=["GET"])
# def display_menu(choice):
#     # 0 for full menu, 1 for specific item
#     menu = {}
#     if choice == 0:
#         menu = {
#             'sizes': sizes,
#             'types': types,
#             'prices': prices,
#             'toppings': toppings
#         }
#     return jsonify(menu)

if __name__ == "__main__":
    app.run()
