import asyncio
import os
import random
import string

import aiohttp

from constants import DATASET_FOLDER


def generate_url(url='http://i.imgur.com/'):
    length = random.choice((5, 6))
    if length == 5:
        url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    else:
        url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
        url += ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
        url += '.jpg'
    return url


async def scrape_pictures():
    INVALID = [0, 503, 5082, 4939, 4940, 4941, 12003, 5556]
    while True:
        url = generate_url()
        filename = url.rsplit('/', 1)[-1]

        async with aiohttp.request('get', url) as response:
            data = await response.read()
            file = os.path.join(DATASET_FOLDER, filename)
            with open(file, 'wb') as file:
                file.write(data)

        file_size = os.path.getsize(file.name)
        if file_size in INVALID:
            print("[-] Invalid: " + url)
            os.remove(file.name)
        else:
            print("[+] Valid: " + url)


async def log_time():
    count = 0
    while True:
        if count % 3 == 0:
            print("{} seconds passed".format(count))
        count += 1
        await asyncio.sleep(1)


async def main():
    tasks = []
    async with aiohttp.ClientSession():
        for i in range(10):
            task = asyncio.create_task(scrape_pictures())
            tasks.append(task)
    tasks.append(log_time())
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
