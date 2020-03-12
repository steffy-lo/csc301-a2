class Drink:
    prices = [2] * len(names)

    def __init__(self, name):
        self.name = name

    def get_price(self):
        return self.prices[self.type]

