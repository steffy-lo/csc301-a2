import uuid
import json


class PizzaParlour:
    def __init__(self):
        drinks_file = open("drink.json", "r")
        self._drinks = json.load(drinks_file)
        drinks_file.close()

        pizza_file = open("pizza.json", "r")
        pizza_menu = json.load(pizza_file)
        self._sizes = pizza_menu["sizes"]
        self._types = pizza_menu["types"]
        self._ingredients = pizza_menu["ingredients"]
        self._toppings = pizza_menu["toppings"]
        pizza_file.close()

    def create_pizza(self, size, type):
        return Pizza(size, type, self._ingredients[type])

    def get_all_drinks(self):
        return self._drinks.keys()

    def get_all_pizzas(self):
        return self._types.keys()

    def get_all_sizes(self):
        return self._sizes.keys()

    def get_all_toppings(self):
        return self._toppings.keys()

    def add_new_pizza(self, name, price, ingredients):
        self._types[name] = price
        self._ingredients[name] = ingredients
        self._update_pizza_data()

    # Can be used to add new drink or change existing drink price
    def set_drink_price(self, name, price):
        self._drinks[name] = price
        drinks_file = open("drink.json", "w")
        json.dump(self._drinks, drinks_file)
        drinks_file.close()

    # Can be used to add new topping or change existing topping price
    def set_topping_price(self, topping, price):
        self._toppings[topping] = price
        self._update_pizza_data()

    def set_size_price(self, size, price):
        self._sizes[size] = price
        self._update_pizza_data()

    def set_type_price(self, type, price):
        self._types[type] = price
        self._update_pizza_data()

    def get_topping_price(self, topping):
        return self._toppings[topping]

    def get_size_price(self, size):
        return self._sizes[size]

    def get_type_price(self, type):
        return self._types[type]

    def get_drink_price(self, drink):
        return self._drinks[drink]

    def _update_pizza_data(self):
        pizza_file = open("pizza.json", "w")
        pizza_data = {
            "sizes": self._sizes,
            "types": self._types,
            "ingredients": self._ingredients,
            "toppings": self._toppings
        }
        json.dump(pizza_data, pizza_file)
        pizza_file.close()


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
