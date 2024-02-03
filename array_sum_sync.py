import time
from random import randint as rnd


_LOW_LIMIT = 1
_HIGH_LIMIT = 100
_ARRAY_SIZE = 1_000_000



def sync_sum(arr):
    sum = 0
    for i in range(len(arr)):
        sum += arr[i]
    return sum


if __name__ == "__main__":
    arr = [rnd(_LOW_LIMIT, _HIGH_LIMIT) for _ in range(1, _ARRAY_SIZE + 1)]
    start_time = time.time()
    result = sync_sum(arr)
    end_time = time.time()
    print(f"Подсчет суммы элементов массива синхронным методом: {result}")
    print(f"Время выполнения расчета - {(end_time - start_time) * 1000:.0f} мс")

    start_time = time.time()
    result = sum(arr)
    end_time = time.time()
    print(f"Подсчет суммы элементов методом sum: {result}")
    print(f"Время выполнения расчета - {(end_time - start_time) * 1000:.0f} мс")
