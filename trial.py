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



'''
<a href='https://pngtree.com/so/High'>High png from pngtree.com/</a>
<a href='https://pngtree.com/so/Music'>Music png from pngtree.com/</a>

https://pngtree.com/freepng/high-sound-vector-icon_3791377.html
https://pngtree.com/element/down?id=NDY5NDUwNg==&type=1&time=1642091304&token=Mzc1ODc0YmVhYzdmYzg3MGZiZmE5NzQyYjE2MDc2MTc=
'''
#
