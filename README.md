# a2-starter

Run the main Flask module by running `python3 PizzaParlour.py`

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py

## Pair Programming

### Feature 1: Cancel Order
### Feature 2: Asking for Menu

## Program Design

### Design Pattern

The design pattern we chose to build this API is the builder pattern. We chose this pattern (over the factory method) mainly because a pizza is an object that essentially involves the same steps to make, differing only in the details (i.e., the toppings). This effectively eliminates the telescopic constructor problem by collecting the many arguments one at a time, and keeps the code much cleaner/maintainable. In addition, we add a class called the Pizza Factory which handles the creation of these pizza along with the support of adding new types of pizzas and toppings.

### Code Cohesion

In our API, the only objects are pizzas and therefore, there are technically no coupling between any objects and this follows into code cohesion.

### Function Design

In our pizza class, we have implemented dependency injection when calculating the price of a pizza, injecting an instance of a pizza factory. This is done as the price of a pizza will depend on given base prices of sizes, type, and topping prices which is determined through the pizza factory. This effectively increases code cohesion.
