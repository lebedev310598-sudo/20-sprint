import asyncio
import time
import aiohttp


async def download_site_async(session, url):
    async with session.get(url) as response:
        content = await response.read()
        print(f"Скачано {len(content)} байт из {url}")


async def asynchronous_download():
    sites = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.create_task(download_site_async(session, url))
            tasks.append(task)

        await asyncio.gather(*tasks)

    duration = time.time() - start_time
    print(f"Асинхронно скачано {len(sites)} сайтов за {duration:.2f} секунд")


if __name__ == "__main__":
    asyncio.run(asynchronous_download())
