# 5. Write a script to remove values duplicates from dictionary.
#  Feel free to hardcode your dictionary.
nums = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 1, "eighth": 2}
new_nums = {}
for key, value in nums.items():
    if value not in new_nums.values():
        new_nums[key] = value
nums = new_nums
# print(nums)
