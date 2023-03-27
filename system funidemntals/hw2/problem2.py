import random


def part_a():
    numbers = []
    number_of_ints = 100
    
    for i in range(number_of_ints):

        numbers.append(random.randint(0, 99))

    return numbers



def part_b():
    numbers = []
    number_of_decimals = 100

    for i in range(number_of_decimals):
        
        numbers.append(round(random.uniform(.25,.5),3))
    
    return numbers




def part_c():
    fixed_numbers = []
    number_of_cases = 100
    
    for i in range(number_of_cases):
        chance = round(random.uniform(0,1),2)

        if (chance <= .5):
            fixed_numbers.append(1)

        elif (chance > .5 and chance <= .7):
            fixed_numbers.append(2)
        
        else:
            fixed_numbers.append(round(random.uniform(3,4),2))
    
    return fixed_numbers




print('below is an array of 100 uniformly distributed integers between 0 and 99.')
print(part_a())
print('below is an array of 100 uniformly distributed floating numbers between 0.25 and 0.5.')
print(part_b())
print('below is an array of  100 numbers in which the number 1 is produced with probability 0.5, the number 2 with probability 0.2, otherwise a floating number between 3 and 4.')
print(part_c())

#all done