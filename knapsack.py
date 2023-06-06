import random

class Knapsack:
    def __init__(self, capacity):
        self.capaciy = capacity
        self.taken_capacity = 0
        self.value = 0
        self.objects = []

    def __str__(self):
        ret = []
        ret.append("Objects list: ")
        for i, (val, weight) in enumerate(self.objects):
            ret.append(f"object {i}: value: {val:.2f} | weight: {weight:.2f}")
        ret.append(f"Total packed: {self.taken_capacity} with value: {self.value}")
        ret = "\n".join(ret)
        return ret

    def __eq__(self, __value: object) -> bool:
        if self.value == __value.value:
            return True
        return False

def map_profit(objects):
    profit = [i/j for i, j in objects]
    return zip(objects, profit)

def knapsack_greedy(objects, knapsack_capacity):
    knapsack = Knapsack(knapsack_capacity)
    sorted_by_profit = sorted(map_profit(objects), key = lambda x: x[1], reverse = True)
    for (val, weight), _ in sorted_by_profit:
        if val < 0:
            break
        if knapsack.taken_capacity + weight > knapsack.capaciy:
            continue
        knapsack.taken_capacity += weight
        knapsack.objects.append((val, weight))
        knapsack.value += val
    return knapsack


def knapsack_forced(objects, knapsack_capacity):
    best = {"nb" : 0, "value": 0, "weight": 0}
    objects.sort(key = lambda x: x[1])
    for attempt in range(1, (2<<len(objects))):
        flag = 0
        attempt = bin(attempt).lstrip('0b')
        attempt = "0"*(len(objects)-len(attempt)) + attempt
        current = {"nb" : attempt, "value": 0, "weight": 0}
        for include, (val, weight) in zip(attempt, objects):
            if include == "1":
                current['value'] += val
                current['weight'] += weight
                if current['weight'] > knapsack_capacity:
                    flag = 1
                    break
        if current['value'] >= best['value'] and not flag:
            best = current

    return build_knapsack(objects, best['nb'], knapsack_capacity)

def knapsack_dynamic(objects, capacity):
    n = len(objects)
    weights = [x[1] for x in objects]
    vals = [x[0] for x in objects]

    tab = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if weights[i - 1] <= j:
                tab[i][j] = max(vals[i - 1] + tab[i - 1][j - weights[i - 1]], tab[i - 1][j])
            else:
                tab[i][j] = tab[i - 1][j]

    knapsack = Knapsack(capacity)
    stored = []
    i, j = n, capacity
    while i > 0 and j > 0:
        if tab[i][j] != tab[i - 1][j]:
            stored.append(objects[i - 1])
            j -= weights[i - 1]
        i -= 1

    stored.reverse()

    for val,weight in stored:
        knapsack.objects.append((val,weight))
        knapsack.value+=val
        knapsack.taken_capacity+=weight

    return knapsack


def build_knapsack(objects, attempt, knapsack_capacity):
    knapsack = Knapsack(knapsack_capacity)
    for include, (val, weight) in zip(attempt, objects):
        if include == "1":
            knapsack.objects.append((val, weight))
            knapsack.taken_capacity+=weight
            knapsack.value+=val
    return knapsack

def main():
    N = 20
    VAL = (1,10)
    WEIGHT  = (1,10)
    CAPACITY = 30
    objects = [(random.randint(*VAL), random.randint(*WEIGHT)) for i in range(N)]
    knapsack = knapsack_forced(objects, CAPACITY)
    print("brute force", knapsack)
    knapsack = knapsack_greedy(objects, CAPACITY)
    print('greedy', knapsack)
    knapsack = knapsack_dynamic(objects, CAPACITY)
    print('dynamic', knapsack)

if __name__ == "__main__":
    main()
