from flask import Flask, jsonify, request

app = Flask("Assignment 2")

orders = []

sizes = ['small', 'medium', 'large']
types = ['pepperoni', 'margherita', 'vegetarian', 'Neapolitan']
toppings = ['olives', 'tomatoes', 'mushrooms', 'jalapenos', 'chicken', 'beef', 'pepperoni']
prices = {'sizes': [1, 2, 3], 'types': [1, 2, 3, 4], 'toppings': [1] * len(toppings)}

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

@app.route('/new_order/<int:id>', methods=["PUT"])
def new_order():

    #check for validity here instead of in Pizza/Drinks classes
    return

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
