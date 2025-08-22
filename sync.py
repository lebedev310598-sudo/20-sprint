import time
import requests


def download_site(url, session):
    with session.get(url) as response:
        print(f"Скачано {len(response.content)} байт из {url}")


def synchronous_download():
    sites = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]

    start_time = time.time()
    session = requests.Session()

    for url in sites:
        download_site(url, session)

    duration = time.time() - start_time
    print(f"Синхронно скачано {len(sites)} сайтов за {duration:.2f} секунд")


if __name__ == "__main__":
    synchronous_download()
