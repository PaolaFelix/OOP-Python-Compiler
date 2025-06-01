class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        print(f"{self.brand} vehicle starting...")

class Car(Vehicle):
    def start(self):
        print(f"{self.brand} car is now running!")

# Usage
my_car = Car("Toyota")
my_car.start()