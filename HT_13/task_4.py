# 4. Create 'list'-like object, but index starts from 1 and index of 0 raises error. 
# Тобто це повинен бути клас, який буде поводити себе так, як list (маючи основні методи), 
# але індексація повинна починатись із 1

class CustomList:
    def __init__(self, *args):
        self.elements = list(args)


    def __getitem__(self, index):
        if index < 1:
            raise IndexError("Index must be greater than or equal to 1")
        try:
            return self.elements[index - 1]
        except IndexError:
            raise IndexError("Index out of range")


    def __setitem__(self, index, value):
        if index < 1:
            raise IndexError("Index must be greater than or equal to 1")
        try:
            self.elements[index - 1] = value
        except IndexError:
            raise IndexError("Index out of range")


    def __str__(self):
        return str(self.elements)


custom_list = CustomList(10, 20, 30, 40, 50)
print(custom_list[1])
print(custom_list[3])
custom_list[2] = 25
print(custom_list)
