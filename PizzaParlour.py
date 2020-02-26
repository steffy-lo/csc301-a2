from flask import Flask

app = Flask("Assignment 2")

orders = []

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

@app.route('/new_order/<int:id>', methods='PUT')
def new_order():

if __name__ == "__main__":
    app.run()
