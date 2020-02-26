class Pizza:
    sizes = ['small', 'medium', 'large']
    types = ['pepperoni', 'margherita', 'vegetarian', 'Neapolitan']
    toppings = ['olives', 'tomatoes', 'mushrooms', 'jalapenos', 'chicken', 'beef', 'pepperoni']
    prices = {'sizes': [1, 2, 3], 'types': [1, 2, 3, 4], 'toppings': [1] * len(toppings)}

    def __init__(self, size, type):
        if size in self.sizes and type in self.types:
            self.size = size
            self.type = type
            self.topping = []
        else:
            print("invalid pizza")

    def add_topping(self, topping):
        if topping in self.toppings:
            self.topping.append(topping)
        else:
            print("invalid topping")
