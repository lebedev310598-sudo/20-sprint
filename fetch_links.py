import requests
from bs4 import BeautifulSoup
import json


class SimpleChunkParser:
    def __init__(self, url, chunk_size=1024):
        self.url = url
        self.chunk_size = chunk_size
        self.session = requests.Session()

    def fetch_data(self):
        """Получение данных чанками"""
        try:
            response = self.session.get(self.url, stream=True)
            response.raise_for_status()

            # Читаем данные чанками
            content = bytearray()
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    content.extend(chunk)
                    # Можно добавить обработку каждого чанка здесь
                    print(f"Получено {len(chunk)} байт")

            # Декодируем весь контент
            return self.decode_content(content, response.encoding)

        except requests.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None

    def decode_content(self, content, encoding='utf-8'):
        """Декодирование контента с обработкой разных кодировок"""
        try:
            # Пытаемся декодировать с указанной кодировкой
            decoded_content = content.decode(encoding)
            return decoded_content
        except UnicodeDecodeError:
            # Если не получается, пробуем другие кодировки
            encodings = ['utf-8', 'cp1251', 'iso-8859-1', 'windows-1251']
            for enc in encodings:
                try:
                    decoded_content = content.decode(enc)
                    print(f"Успешно декодировано с кодировкой: {enc}")
                    return decoded_content
                except UnicodeDecodeError:
                    continue
            print("Не удалось декодировать контент")
            return None

    def parse_html(self, html_content):
        """Парсинг HTML контента"""
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        # Пример извлечения данных
        data = {
            'title': soup.find('title').get_text() if soup.find('title') else 'No title',
            'links': [a.get('href') for a in soup.find_all('a', href=True)],
            'text_content': soup.get_text()[:500] + '...'  # Первые 500 символов
        }

        return data

    def save_to_file(self, data, filename):
        """Сохранение данных в файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(data, dict):
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    f.write(str(data))
            print(f"Данные сохранены в {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")


# Использование
if __name__ == "__main__":
    # Пример URL (замените на нужный)
    url = "https://example.com"

    parser = SimpleChunkParser(url, chunk_size=512)

    # Получаем данные
    html_content = parser.fetch_data()

    if html_content:
        # Парсим HTML
        parsed_data = parser.parse_html(html_content)

        # Сохраняем результаты
        parser.save_to_file(parsed_data, 'parsed_data.json')

        # Выводим результаты
        print(f"Заголовок: {parsed_data['title']}")
        print(f"Найдено ссылок: {len(parsed_data['links'])}")
        print(f"Текст: {parsed_data['text_content']}")
