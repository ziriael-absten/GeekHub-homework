# 1. Напишіть програму, де клас «геометричні фігури» (Figure) містить властивість color з 
# початковим значенням white і метод для зміни кольору фігури, а його підкласи «овал» 
# (Oval) і «квадрат» (Square) містять методи __init__ для
# завдання початкових розмірів об'єктів при їх створенні.

class Figure:
    def __init__(self):
        self.color = "white"


    def change_color(self, new_color):
        self.color = new_color


class Oval(Figure):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height


class Square(Figure):
    def __init__(self, side_length):
        super().__init__()
        self.side_length = side_length


oval_object = Oval(width=10, height=15)
square_object = Square(side_length=8)
oval_object.change_color("blue")
square_object.change_color("red")
print(f"Oval color: {oval_object.color}, Width: {oval_object.width}, Height: {oval_object.height}")
print(f"Square color: {square_object.color}, Side Length: {square_object.side_length}")
