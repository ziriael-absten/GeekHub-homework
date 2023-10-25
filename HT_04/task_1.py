# Написати скрипт, який приймає від користувача два числа (int або float) і робить наступне:
# Кожне введене значення спочатку пробує перевести в int. У разі помилки - пробує перевести 
# в float, а якщо і там ловить помилку - пропонує ввести значення ще раз (зручніше на даному
#  етапі навчання для цього використати цикл while)
# Виводить результат ділення першого на друге. Якщо при цьому виникає помилка - оброблює її 
# і виводить відповідне повідомлення
while True:
    first_num = input("Enter first num: ")
    second_num = input("Enter second num: ")
    try:
        first_num = int(first_num)
        second_num = int(second_num)
    except ValueError:
        try:
            first_num = float(first_num)
            second_num = float(second_num)
        except ValueError:
            print("Enter valid numbers please")
            continue
    try:
        print(f"{first_num / second_num}")
        break
    except Exception as error:
        print(f"Error : {error}")
        break


