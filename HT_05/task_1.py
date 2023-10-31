# 1. Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 до 12) та 
# яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь). 
# У випадку некоректного введеного значення - виводити відповідне повідомлення.

def season(month_num):
    if month_num in [1, 2, 12]:
        return "Winter"
    if month_num in [3, 4, 5]:
        return "Spring"
    if month_num in [6, 8, 7]:
        return "Summer"
    if month_num in [9, 10, 11]:
        return "Autumn"
    else:
        return("Value is not correct")

month = input("Enter a number of month: ")
try:
    month = int(month)
except ValueError:
    print("Invalid values")
else:
    print(season(month))
