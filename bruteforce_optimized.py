import time

class Knapsack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.taken_capacity = 0
        self.value = 0
        self.objects = []

    def __str__(self):
        ret = []
        ret.append("Objects list: ")
        for i, (val, weight) in enumerate(self.objects):
            ret.append(f"object {i}: value: {val:.2f} | weight: {weight:.2f}")
        ret.append(f"Total packed (weight): {self.taken_capacity} with value: {self.value}")
        ret = "\n".join(ret).lstrip("\n")
        return ret
    
    def __eq__(self, __value: object) -> bool:
        if self.value == __value.value:
            return True
        return False

def build_knapsack(objects, attempt, knapsack_capacity):
    knapsack = Knapsack(knapsack_capacity)
    for include, (val, weight) in zip(attempt, objects):
        if include == "1":
            knapsack.objects.append((val, weight))
            knapsack.taken_capacity+=weight
            knapsack.value+=val
    return knapsack

def knapsack_util(objects, capacity):
    stored = [0]*((1<<len(objects)))
    stored[0] = (0,0,0) #id sum(val) sum(weight)
    for attempt in range(1, (1<<len(objects))):
        flag = 0
        current = [attempt,0 , 0]
        attempt = bin(attempt).lstrip('0b')
        attempt = "0"*(len(objects)-len(attempt)) + attempt
        for include, (val, weight) in zip(attempt, objects):
            if include == "1":
                current[1] += val
                current[2] += weight
                if current[2] > capacity:
                    stored[current[0]] = (current[0],-1, 0)
                    flag = 1
                    break
        if not flag:
            stored[current[0]] = tuple(current)
    stored = [(nb, val, weight) for nb, val, weight in stored if val>=0]
    stored.sort(key = lambda x: x[1], reverse=True)
    return stored
        

def knapsack_fastforced(objects, knapsack_capacity): 
    best = ([0,0],0,0)
    A = knapsack_util(objects[:len(objects)//2], knapsack_capacity)
    B = knapsack_util(objects[len(objects)//2:], knapsack_capacity)
    for anb, aval, aweigth in A:
        for bnb, bval, bweigth in B:
            if aval+bval<=best[1]:
                break
            if aweigth+bweigth <= knapsack_capacity:
                best=([anb, bnb], aval+bval, aweigth+bweigth) 
                break

    codea =  bin(best[0][0]).lstrip('0b')
    codea = "0"*(len(objects[:len(objects)//2])-len(codea)) + codea
    codeb =  bin(best[0][1]).lstrip('0b')
    codeb = "0"*(len(objects[len(objects)//2:])-len(codeb)) + codeb

    return build_knapsack(objects, codea+codeb, knapsack_capacity)


def read_objects():
    objects = []
    capacity = 0
    with open("data.txt", 'r') as file:
        capacity = int(file.readline())
        file.readline()
        for i in file.readlines():
            i = i.split()
            val = int(i[0])
            weight = int(i[1])
            objects.append((val, weight))
    return objects, capacity

def main():
    objects, capacity = read_objects()
    now = time.time()
    knapsack = knapsack_fastforced(objects, capacity)
    print(knapsack)
    print(f'Time: {time.time()-now}s')

if __name__ == "__main__":
    main()


