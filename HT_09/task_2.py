# 2. Написати функцію, яка приймає два параметри: ім'я (шлях) файлу та кількість символів. 
# Файл також додайте в репозиторій. На екран повинен вивестись список із трьома блоками - 
# символи з початку, із середини та з кінця файлу. Кількість символів в блоках - та, яка 
# введена в другому параметрі. Придумайте самі, як обробляти помилку, наприклад, коли 
# кількість символів більша, ніж є в файлі або, наприклад, файл із двох символів і треба 
# вивести по одному символу, то що виводити на місці середнього блоку символів?). Не 
# забудьте додати перевірку чи файл існує.

import os


def text_blocks(f, num):
    if not os.path.exists(f):
        print(f"File {f} doesn't exist")
        return
    with open(f) as my_file:
        content = my_file.read()
        if num <= 0:
            print("Num of symbols should be mmore then 0")
            return
        if num > len(content):
            print("Num of symbols is more then length of file")
            return
        start = content[0:num]
        end = content[-num:]
        middle_len = len(content) // 2
        middle  = content[middle_len - num // 2:middle_len + num // 2]
        return [start, middle, end]


print(text_blocks("HT_09/example1.txt", 2))
