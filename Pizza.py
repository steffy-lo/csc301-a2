import uuid


class PizzaFactory:
    def __init__(self):
        self._sizes = {'small': 4, 'medium': 5.5, 'large': 7}
        self._types = {'pepperoni': 0.5,
                       'margherita': 1,
                       'vegetarian': 0.2,
                       'neapolitan': 1.5}
        self._ingredients = {'pepperoni': ["cheese", "pepperoni"],
                             'margherita': ["tomatoes", "cheese", "basil"],
                             'vegetarian': ["tomatoes", "spinach", "onions"],
                             'neapolitan': ["neapeolitan sauce", "cheese", "basil"]}
        self._toppings = {'olives': 0.1,
                          'tomatoes': 0.1,
                          'mushrooms': 0.1,
                          'jalapenos': 0.1,
                          'chicken': 0.1,
                          'beef': 0.1,
                          'pepperoni': 0.1}

    def create_pizza(self, size, type):
        return Pizza(size, type, self._ingredients[type])

    def get_all_pizzas(self):
        return self._types.keys()

    def get_all_sizes(self):
        return self._sizes.keys()

    def get_all_toppings(self):
        return self._toppings.keys()

    def add_new_pizza(self, name, price, ingredients):
        self._types[name] = price
        self._ingredients[name] = ingredients

    # Can be used to add new topping or change existing topping price
    def set_topping_price(self, topping, price):
        self._toppings[topping] = price

    # Can be used to add new size or change existing size price
    def set_size_price(self, size, price):
        self._sizes[size] = price

    def set_type_price(self, type, price):
        if type not in self._types:
            print("Not valid type of pizza!")
            return
        self._types[type] = price

    def get_topping_price(self, topping):
        return self._toppings[topping]

    def get_size_price(self, size):
        return self._sizes[size]

    def get_type_price(self, type):
        return self._types[type]


class Pizza:
    def __init__(self, size, type, ingredients):
        self.size = size
        self.type = type
        self.itemID = str(uuid.uuid4())
        self.ingredients = ingredients
        self.toppings = []

    def add_topping(self, topping):
        self.toppings.append(topping)

    def remove_topping(self, topping):
        self.toppings.remove(topping)

    def get_price(self, pizza_factory):
        size_price = pizza_factory.get_size_price(self.size)
        type_price = pizza_factory.get_type_price(self.type)
        toppings_price = 0
        for topping in self.toppings:
            toppings_price += pizza_factory.get_topping_price(topping)
        return size_price + type_price + toppings_price
