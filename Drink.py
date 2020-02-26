class Drink:
    names = ['Coke', 'Diet Coke', 'Coke Zero', 'Pepsi', 'Diet Pepsi', 'Dr. Pepper', 'Water, Juice']
    prices = [2] * len(names)

    def __init__(self, name):
        if name in self.names:
            self.name = name
            self.type = self.names.index(name)
        else:
            print("drink is unavailable")

    def get_price(self):
        return self.prices[self.type]

