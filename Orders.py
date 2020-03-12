import uuid

class Pizza:
    def __init__(self, size, type):
        self.size = size
        self.type = type
        self.itemID = str(uuid.uuid4())
        self.ingredients = []
        self._set_ingredients(type)
        self.toppings = []
        
    def add_topping(self, topping):
        self.toppings.append(topping)

    def remove_topping(self, topping):
        self.toppings.remove(topping)

    def _set_ingredients(self, type):
        if type == "pepperoni":
            self.ingredients.append("pepperoni")
            self.ingredients.append("cheese")
        elif type == "margherita":
            self.ingredients.append("tomatoes")
            self.ingredients.append("cheese")
            self.ingredients.append("basil")
        elif type == "vegetarian":
            self.ingredients.append("tomatoes")
            self.ingredients.append("spinach")
            self.ingredients.append("onions")
        elif type == "neapolitan":
            self.ingredients.append("neapeolitan sauce")
            self.ingredients.append("cheese")
            self.ingredients.append("basil")


