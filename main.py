import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Список ключевых слов строго по шаблону задания
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Ссылка на поток "Все подряд", где нет лишнего мусора из плиток
URL = "https://habr.com/ru/all/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

try:
    # 1. Исправлено: добавлен таймаут во избежание зависания сети
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Поддерживает и старую верстку из задания, и актуальную
    articles = soup.find_all("article")
    
    for article in articles:
        title_tag = article.find("h2")
        if not title_tag:
            continue
        title = title_tag.text.strip()
        
        # Безопасное извлечение ссылки, узел проверяется на None
        link_tag = title_tag.find("a") if title_tag else None
        href = link_tag.get("href") if link_tag else None
        
        if href:
            # Автоматически обрабатывает и относительные, и абсолютные ссылки
            link = urljoin("https://habr.com", href)
        else:
            link = "Ссылка отсутствует"
            
        # Фолбэк для даты: извлекает title, если его нет — datetime или чистый текст
        time_tag = article.find("time")
        date = "Дата не указана"
        if time_tag:
            date = time_tag.get("title") or time_tag.get("datetime") or time_tag.text.strip()
            
        card_text = article.text.lower()
        
        # Исправлено: корректный поиск границ слов для кириллицы и латиницы
        matches_keyword = False
        for keyword in KEYWORDS:
            kw_clean = keyword.lower()
            pattern = rf"(?<![a-zа-яё]){re.escape(kw_clean)}(?![a-zа-яё])"
            if re.search(pattern, card_text):
                matches_keyword = True
                break
        
        if matches_keyword:
            # Вывод строго в формате задания: <дата> - <заголовок> - <ссылка>
            print(f"{date} - {title} - {link}")

# 2. Исправлено: перехват сетевых исключений вместо падения с трейсбеком
except requests.RequestException as e:
    print(f"Не удалось получить данные. Ошибка сети: {e}")
