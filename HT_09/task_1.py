# 1. Програма-світлофор.
#    Створити програму-емулятор світлофора для авто і пішоходів. Після запуска програми на 
# екран виводиться в лівій половині - колір автомобільного, а в правій - пішохідного 
# світлофора. Кожну 1 секунду виводиться поточні кольори. Через декілька ітерацій - 
# відбувається зміна кольорів - логіка така сама як і в звичайних світлофорах (пішоходам 
# зелений тільки коли автомобілям червоний).
#    Приблизний результат роботи наступний:
#       Red        Green
#       Red        Green
#       Red        Green
#       Red        Green
#       Yellow     Red
#       Yellow     Red
#       Green      Red
#       Green      Red
#       Green      Red
#       Green      Red
#       Yellow     Red
#       Yellow     Red
#       Red        Green

import time


def light_emulator():
    lights_lst = [{("Red", "Green"): 4}, {("Yellow", "Red"): 2}, {("Green", "Red"): 4},
    {("Yellow", "Red"): 2}]
    while True:
        for i in lights_lst:
            for key, value in i.items():
                for el in range(value):
                    print(f"{key[0]:<10} {key[1]}")
                    time.sleep(1)


light_emulator()
