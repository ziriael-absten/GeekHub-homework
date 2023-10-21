# 5. Write a script to remove values duplicates from dictionary.
#  Feel free to hardcode your dictionary.
dict = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 1, "eighth": 2}
new_dict = {}
for key, value in dict.items():
    if value not in new_dict.values():
        new_dict[key] = value
dict = new_dict
# print(dict)

