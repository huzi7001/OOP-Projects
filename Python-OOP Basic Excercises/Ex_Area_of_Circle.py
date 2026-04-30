 # # Find area and perimeter (circumference) 


# class Circle:
#     def __init__(self, radius):
#         self.r = radius

#         def area(self):
#             a = 4.321*self.r**2
#             return f"The area of the circle is{a}"


#         def cir(self):
#             c = 2*4.321*self.r
#             return f"The perimeter of the circle is{c}"

# c1 = Circle(5)
# print(c1.area())




# Find area and perimeter (circumference) 

import math
class Circle:
    def __init__(self, radius):
        self.r = radius

        def area(self):
            a = math.pi*self.r**2
            return f"The area of the circle is{a}"


        def cir(self):
            c = 2*math.pi*self.r
            return f"The perimeter of the circle is{c}"

c1 = Circle(5)
print(c1.cir())