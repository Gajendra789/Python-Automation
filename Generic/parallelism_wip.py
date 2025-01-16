import threading

def print_numbers():
    for i in range(5):
        print(i)

# Create threads
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_numbers)

# Start threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()


---------------

import multiprocessing

def square(number):
    print(number * number)

if __name__ == "__main__":
    # Create a pool of workers
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(square, [1, 2, 3, 4, 5])

-----------

from concurrent.futures import ThreadPoolExecutor

def task(number):
    return number * 2

# Using ThreadPoolExecutor for concurrency
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(task, [1, 2, 3, 4, 5])

for result in results:
    print(result)

----------------------
import asyncio

async def task(number):
    await asyncio.sleep(1)
    print(number * 2)

async def main():
    tasks = [task(i) for i in range(5)]
    await asyncio.gather(*tasks)

# Run the event loop
asyncio.run(main())

