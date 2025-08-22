import time
import requests
from multiprocessing import Pool, cpu_count


def download_site_mp(url):
    try:
        response = requests.get(url)
        print(f"Скачано {len(response.content)} байт из {url}")
        return len(response.content)
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return 0


def multiprocess_download():
    sites = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]

    start_time = time.time()

    # Используем количество процессов равное количеству CPU
    num_processes = min(cpu_count(), len(sites))

    with Pool(processes=num_processes) as pool:
        results = pool.map(download_site_mp, sites)

    total_bytes = sum(results)
    duration = time.time() - start_time

    print(f"Мультипроцессорно скачано {len(sites)} сайтов")
    print(f"Всего скачано {total_bytes} байт за {duration:.2f} секунд")


if __name__ == "__main__":
    multiprocess_download()
