# 2. Write a script to remove an empty elements from a list.
#     Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
test_lst = [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
new_lst = []
for i in test_lst:
    if len(i) != 0:
        new_lst.append(i)
test_lst = new_lst
# print(test_lst)

