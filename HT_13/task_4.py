# 4. Create 'list'-like object, but index starts from 1 and index of 0 raises error. 
# Тобто це повинен бути клас, який буде поводити себе так, як list (маючи основні методи), 
# але індексація повинна починатись із 1

class CustomList:
    def __init__(self, *args):
        self.elements = list(args)


    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start - 1 if index.start is not None else None
            stop = index.stop - 1 if index.stop is not None else None
            step = index.step
            return self.elements[start:stop:step]
        elif -len(self.elements) <= index < 0:
            return self.elements[index]
        elif index == 0:
            raise IndexError("Index must be greater or smaller than 0")
        try:
            return self.elements[index - 1]
        except IndexError:
            raise IndexError("Index out of range")


    def __setitem__(self, index, value):
        if -len(self.elements) <= index < 0:
            self.elements[index] = value
        elif index == 0:
            raise IndexError("Index must be greater or smaller than 0")
        try:
            self.elements[index - 1] = value
        except IndexError:
            raise IndexError("Index out of range")


    def __iter__(self):
        return iter(self.elements)


    def __str__(self):
        return str(self.elements)


custom_list = CustomList(10, 20, 30, 40, 50)
print(custom_list[-1])
print(custom_list[-3])
print(custom_list[-3:])
custom_list[-2] = 35
print(custom_list)
for element in custom_list:
    print(element)
    