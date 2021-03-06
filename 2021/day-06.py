from collections import Counter


def input():
    with open("input-06.txt") as lines:
        for line in lines:
            yield line.strip()


fish = Counter()
for line in input():
    for i in line.split(","):
        fish[int(i)] += 1


def tick(fish):
    delta = Counter()
    for day, count in fish.items():
        if day == 0:
            delta[6] += count
            delta[8] += count
        else:
            delta[day - 1] += count
    return delta


for _ in range(80):
    fish = tick(fish)
print("1:", sum(fish.values()))

for _ in range(256 - 80):
    fish = tick(fish)
print("1:", sum(fish.values()))
