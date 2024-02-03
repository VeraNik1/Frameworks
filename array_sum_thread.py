import threading
import time
from random import randint as rnd

_LOW_LIMIT = 1
_HIGH_LIMIT = 100
_ARRAY_SIZE = 1_000_000
_STEP = 200_000


def summ_numbers(arr, limit_1, limit_2):
    summ = 0
    for i in range(limit_1, limit_2):
        summ += arr[i]
    summ_list.append(summ)


limit_1 = 0
limit_2 = limit_1 + _STEP

threads = []
summ_list = []

if __name__ == "__main__":
    while limit_2 <= _ARRAY_SIZE:
        arr = [rnd(_LOW_LIMIT, _HIGH_LIMIT) for _ in range(1, _ARRAY_SIZE + 1)]
        start_time = time.time()
        thread = threading.Thread(target=summ_numbers, args=[arr, limit_1, limit_2])
        threads.append(thread)
        thread.start()
        limit_1, limit_2 = limit_2, limit_2 + _STEP

    for thread in threads:
        thread.join()
    end_time = time.time()
    print(f"Подсчет суммы элементов массива методом разделения потоков: {sum(summ_list)}")
    print(f"Время выполнения расчета - {(end_time - start_time) * 1000:.0f} мс")
