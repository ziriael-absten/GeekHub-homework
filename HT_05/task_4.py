# 4. Наприклад маємо рядок --> "f98neroi4nr0c3n30irn03ien3c0rfe  kdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p4 65jnpoj35po6j345" -> просто потицяв по клавi =)
#    Створіть ф-цiю, яка буде отримувати рядки на зразок цього та яка оброблює наступні випадки:
# -  якщо довжина рядка в діапазонi 30-50 (включно) -> прiнтує довжину рядка, кiлькiсть букв та цифр
# -  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр лише з буквами (без пробілів)
# -  якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію =)

def string_processing(string):
    if len(string) >= 30 and len(string) <= 50:
        letter_sum = 0
        num_sum = 0
        for i in string:
            if i.isdigit():
                num_sum += 1
            if i.isalpha():
                letter_sum += 1
        print(f"""Length of this string is {len(string)} symbols\nAmount of numbers is {num_sum}\nAmount of letters is {letter_sum}""")
    if len(string) < 30:
        num_sum = 0
        str = ""
        for i in string:
            if i.isdigit():
                num_sum += int(i)
            if i.isalpha():
                str += i
        print(f"""Numbers sum is {num_sum}\nString without numbers is '{str}'""")
    else:
        symbol = input("Enter a letter or a number: ")
        amount_in_str = string.count(symbol)
        print(f"There are {amount_in_str} '{symbol}' in string")

# string_processing("f98neroi4nr0c3n30irn0")
# string_processing("f98neroi4nr0c3n30irn03ien3c0rfe  kdno4")
# string_processing("f98neroi4nr0c3n30irn03ien3c0rfe  kdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p4 65jnpoj35po6j345")
