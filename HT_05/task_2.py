# 2. Створiть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна повертати 
# якийсь результат (напр. інпут від юзера, результат математичної операції тощо). 
# Також створiть четверту ф-цiю, яка всередині викликає 3 попереднi,
# обробляє їх результат та також повертає результат своєї роботи. Таким чином ми будемо 
# викликати одну (четверту) функцiю, а вона в своєму тiлi - ще 3.

import random


def random_num():
    return random.randint(1, 100)

def hundred(num):
    return 100 - num

def subtraction(first, second):
    return first - second

def sum():
    return random_num() + hundred(68) + subtraction(20, 30)

print(sum())
