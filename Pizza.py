class Pizza:

    def __init__(self, size, type):
        self.size = size
        self.type = type
        self.topping = []
        
    def add_topping(self, topping):
        self.topping.append(topping)

