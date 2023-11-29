# 3. Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів 
# класів.

class MyClass:
    instances_count = 0

    def __init__(self):
        MyClass.instances_count += 1


obj1 = MyClass()
obj2 = MyClass()
obj3 = MyClass()
print(f"Number of class instances: {MyClass.instances_count}")
