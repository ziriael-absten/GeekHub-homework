# 6. Напишіть функцію,яка прймає рядок з декількох слів і повертає довжину найкоротшого 
# слова. Реалізуйте обчислення за допомогою генератора.

def shortest(string):
    word_lengths = (len(word) for word in string.split())
    return min(word_lengths)


sentence = "Python is a programming language"
print(shortest(sentence))
