import copy

number = 1
print(f"{number:02d}")

print(min(12, 3))

class Car():
    def __init__(self, no):
        self.color = "Blue"
        self.no = no
        
    def increment(self, no):
        self.no = self.no + no
    

car1 = Car(3)
print(car1)
car2 = copy.deepcopy(car1)
print(car2)


#
