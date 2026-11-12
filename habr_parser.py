import requests
from bs4 import BeautifulSoup

# Определяем список ключевых слов в начале скрипта
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = 'https://habr.com/ru/articles/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# Находим все блоки статей на странице
articles = soup.find_all('article')

for article in articles:
    # Собираем весь текст из preview-информации статьи и переводим в нижний регистр
    preview_text = article.text.lower()
    
    # Проверяем, встречается ли хотя бы одно ключевое слово
    if any(word.lower() in preview_text for word in KEYWORDS):
        # Извлекаем дату публикации
        time_tag = article.find('time')
        date = time_tag.get('title') if time_tag and time_tag.has_attr('title') else (time_tag.text.strip() if time_tag else 'Дата не найдена')
        
        # Извлекаем заголовок и ссылку
        title_tag = article.find('h2')
        if title_tag and title_tag.find('a'):
            link_tag = title_tag.find('a')
            title = link_tag.text.strip()
            href = link_tag.get('href')
            # Если ссылка относительная, добавляем домен
            link = f'https://habr.com{href}' if href.startswith('/') else href
            
            print(f'{date} – {title} – {link}')