import multiprocessing as mp
import time
from random import randint as rnd

_LOW_LIMIT = 1
_HIGH_LIMIT = 100
_ARRAY_SIZE = 1_000_000
_STEP = 200_000


def summ_numbers(q, arr, limit_1, limit_2):
    summ = 0
    for i in range(limit_1, limit_2):
        summ += arr[i]
    q.put(summ)



limit_1 = 0
limit_2 = limit_1 + _STEP

processes = []
start_time = time.time()

if __name__ == "__main__":
    arr = [rnd(_LOW_LIMIT, _HIGH_LIMIT) for _ in range(1, _ARRAY_SIZE + 1)]
    start_time = time.time()
    mp.set_start_method('spawn')
    q = mp.Queue()
    res = 0
    while limit_2 <= _ARRAY_SIZE:
        process = mp.Process(target=summ_numbers, args=(q, arr, limit_1, limit_2))
        process.start()
        limit_1, limit_2 = limit_2, limit_2 + _STEP
        res += q.get()

    for process in processes:
        process.join()
    end_time = time.time()
    print(f"Подсчет суммы элементов массива методом разделения процессов: {res}")
    print(f"Время выполнения расчета - {(end_time-start_time) * 1000:.0f} мс")