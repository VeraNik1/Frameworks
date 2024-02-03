import asyncio
import time
from random import randint as rnd


_LOW_LIMIT = 1
_HIGH_LIMIT = 100
_ARRAY_SIZE = 1_000_000
_STEP = 200_000


async def summ_numbers(arr, limit_1, limit_2):
    global summ
    for i in range(limit_1, limit_2):
        summ += arr[i]
    return summ

async def main(arr):
    limit_1 = 0
    limit_2 = limit_1 + _STEP
    tasks = []
    while limit_2 <= _ARRAY_SIZE:
        task = asyncio.create_task(summ_numbers(arr, limit_1, limit_2))
        tasks.append(task)
        limit_1, limit_2 = limit_2, limit_2 + _STEP
    await asyncio.gather(*tasks)
summ = 0



if __name__ == "__main__":
    arr = [rnd(_LOW_LIMIT, _HIGH_LIMIT) for _ in range(1, _ARRAY_SIZE + 1)]
    start_time = time.time()
    asyncio.run(main(arr))
    end_time = time.time()
    print(f"Подсчет суммы элементов массива методом асинхронного программирования: {summ}")
    print(f"Время выполнения расчета - {(end_time - start_time) * 1000:.0f} мс")