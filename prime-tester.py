import math

def isprime(n):
    for i in range(2, int(n / 2.0)):
        if n % i == 0:
            return False
    return True

building_blocks = [1,3,7]
num_digits = 3

num_permutations = len(building_blocks) ** (num_digits)
print(num_permutations)

def appendall(init_num, combo_array):
    new_nums = []
    for i in range(0, len(combo_array)):
        new_nums.append(init_num * 10 + combo_array[i])
    return new_nums

numbers = building_blocks[:]
for i in range(num_digits - 1):
    temp = numbers[:]
    for num in temp:
        numbers += appendall(num, building_blocks)
print(numbers)

for number in sorted(list(set(numbers))):
    if not isprime(number):
        print(number)


