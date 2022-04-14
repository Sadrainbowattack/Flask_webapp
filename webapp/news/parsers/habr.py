from bs4 import BeautifulSoup
from datetime import datetime

from webapp import db
from webapp.news.models import News

from webapp.news.parsers.utils import save_news
from webapp.news.parsers.utils import get_html

def get_habr_snippets():
    html = get_html('https://habr.com/ru/search/?q=python&target_type=posts&order=date')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_='tm-articles-list').findAll('article', class_='tm-articles-list__item')
        for news in all_news:
            title = news.find('a', class_='tm-article-snippet__title-link').text
            url = news.find('a', class_='tm-article-snippet__title-link')['href']
            url = "https://habr.com" + url
            published = news.find('time')['title']
            try:
                published = datetime.strptime(published, "%Y-%m-%d, %H:%M")
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)

def get_habr_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            try:
                article = soup.find('div', class_='article-formatted-body article-formatted-body_version-2').decode_contents()
            except AttributeError:
                article = soup.find('div', class_='article-formatted-body article-formatted-body_version-1').decode_contents()
                
            if article:
                news.text = article
                db.session.add(news)
                db.session.commit()