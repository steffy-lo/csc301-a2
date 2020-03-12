from flask import Flask, jsonify, request, abort

app = Flask("Assignment 2")

orders = []

sizes = {'small': 4, 'medium': 5.5, 'large': 7}
types = {'pepperoni': 0.5, 'margherita': 0.5, 'vegetarian': 0.2, 'neapolitan': 0.5}
toppings = {'olives': 0.1, 'tomatoes': 0.1, 'mushrooms': 0.1, 'jalapenos': 0.1, 'chicken': 0.1, 'beef': 0.1, 'pepperoni': 0.1}
drinks = {'coke': 2, 'diet coke': 2, 'coke zero': 2, 'pepsi': 2, 'diet pepsi': 2, 'dr. pepper': 3.5, 'water': 1, 'juice': 4}

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

@app.route('/new_order', methods=['POST'])
def new_order():
    # request.args.get
    order = request.get_json()
    # request body format example
    # {
    #     "pizzas": [{"size": "small", "type": "pepperoni", "toppings": ["olives", "tomatoes"]}],
    #     "drinks": ["Coke", "Pepsi"]
    # }

    orderNum = len(orders)
    order['orderNum'] = orderNum

    total = 0
    if 'pizzas' in order:
        pizza_orders = order['pizzas']
        for p in pizza_orders:
            # check for validity of order
            if p['size'] not in sizes or p['type'] not in types:
                abort(400)  # bad request
                return
            total += sizes[p['size']]
            total += types[p['type']]
            for topping in p['toppings']:
                # check for validity of toppings
                if topping not in toppings:
                    abort(400)
                    return
                total += toppings[topping]

    if 'drinks' in order:
        drink_orders = order['drinks']
        for d in drink_orders:
            if d not in drinks:
                abort(400)
                return
            total += drinks[d]

    order['price'] = total
    orders.append(order)

    return jsonify(order)

@app.route('/display_menu/<int:choice>', methods=["GET"])
def display_menu(choice):
    # 0 for full menu, 1 for specific item
    menu = {}
    if choice == 0:
        menu = {
            'sizes': sizes,
            'types': types,
            'prices': prices,
            'toppings': toppings
        }
    return jsonify(menu)

if __name__ == "__main__":
    app.run()
