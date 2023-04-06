from copy import deepcopy
from time import process_time as time

grid = [
    [0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 1, 2, 1, 1],
    [1, 2, 1, 2, 1, 2, 2],
    [2, 2, 1, 2, 1, 2, 1],
    [1, 1, 2, 1, 1, 2, 2],
    [1, 2, 1, 2, 2, 1, 1],
]
repetitions = 100000


def custom_copy(obj):
    obj = [list(k) for k in obj]
    return obj


print("DEEPCOPY MODULE:")
start_time = time()
for _ in range(repetitions):
    grid_copy = deepcopy(grid)
end_time = time()
print((end_time - start_time) / repetitions)

print("CUSTOM:")
start_time = time()
for _ in range(repetitions):
    grid_copy = custom_copy(grid)
end_time = time()
print((end_time - start_time) / repetitions)
