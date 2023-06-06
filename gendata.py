import random
def write_objects():
    N = 33
    VAL = (1,20)
    WEIGHT  = (1,30)
    CAPACITY = 300
    objects = [(random.randint(*VAL), random.randint(*WEIGHT)) for i in range(N)]
    with open("data.txt", 'w') as file:
        file.write(f'{CAPACITY}\n')
        file.write(f'{N}\n')
        for i, j in objects:
            file.write(f'{i} {j}\n')

write_objects()