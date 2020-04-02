# a2-starter

Run the main Flask module by running `python3 PizzaParlour.py`

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py

## Pair Programming

### Feature 1: Cancel Order
#### Main Functionality
Driver: Bianca  Navigator: Steffy

#### Testing
Driver: Steffy  Navigator: Bianca
It went pretty smoothly. We liked how the test methods were immediately working as expected. We just had to make sure a thorough test coverage.

### Feature 2: Asking for Menu
#### Main Functionality
Driver: Bianca  Navigator: Steffy
It went quite well. We spent a fair amount of time discussing how to structure the data for displaying the menu. Once we've agreed on the best approach, it was quite smooth sailing with Steffy as the navigator catching any small errors while Bianca was driving the code. However, there were a lot of cases we had to cover, which became tiresome to do after a while.

#### Testing (in 2 Parts)
Driver: Bianca --> Steffy Navigator: Steffy --> Bianca
Getting through all the code coverage was quite a pain, although everything during testing mostly went through as expected so it was good. There was a small problem we had with floating point numbers with Python but that got quickly resolved once we changed the numbers we used during assertion. There were also other small problems we encountered with getting our methods to pass our tests but soon enough realize that it was mostly minor errors like spelling and invalid mock data in our test methods that were causing the tests to fail.

## Program Design

### Design Pattern

The design pattern we chose to build this API is the builder pattern. We chose this pattern (over the factory method) mainly because a pizza is an object that essentially involves the same steps to make, differing only in the details (i.e., the toppings). This effectively eliminates the telescopic constructor problem by collecting the many arguments one at a time, and keeps the code much cleaner/maintainable. In addition, we add a class called the Pizza Factory which handles the creation of these pizza along with the support of adding new types of pizzas and toppings.

### Code Cohesion

In our API, the only objects are pizzas and therefore, there are technically no coupling between any objects and this follows into code cohesion.

### Function Design

In our pizza class, we have implemented dependency injection when calculating the price of a pizza, injecting an instance of a pizza factory. This is done as the price of a pizza will depend on given base prices of sizes, type, and topping prices which is determined through the pizza factory. This effectively increases code cohesion.

## Code Craftmanship

Steffy: Solely used PyCharm IDE to help with programming and formatting style
