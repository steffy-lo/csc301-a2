from PizzaParlour import app
import PizzaParlour

def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'

def test_new_valid_order():
    mock_data = {
        "pizzas": [
            {"size": "small", "type": "pepperoni", "toppings": ["olives", "tomatoes"]},
            {"size": "small", "type": "margherita", "toppings": ["olives", "tomatoes"]},
            {"size": "small", "type": "vegetarian", "toppings": ["olives", "tomatoes"]},
            {"size": "small", "type": "neapolitan", "toppings": ["olives", "tomatoes"]}
                   ],
        "drinks": ["coke", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 200

def test_invalid_size():
    # invalid size
    mock_data = {
        "pizzas": [{"size": "tall", "type": "pepperoni", "toppings": ["olives", "tomatoes"]}],
        "drinks": ["coke", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 400


def test_invalid_type():
    # invalid type
    mock_data = {
        "pizzas": [{"size": "tall", "type": "meat lover", "toppings": ["olives", "tomatoes"]}],
        "drinks": ["coke", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 400


def test_invalid_topping():
    # invalid topping
    mock_data = {
        "pizzas": [{"size": "small", "type": "pepperoni", "toppings": ["cheese", "tomatoes"]}],
        "drinks": ["coke", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 400


def test_invalid_drink():
    # invalid drink
    mock_data = {
        "pizzas": [{"size": "small", "type": "pepperoni", "toppings": ["olives", "tomatoes"]}],
        "drinks": ["7up", "pepsi"]
    }
    response = app.test_client().post('/new_order', json=mock_data)
    assert response.status_code == 400
