from webapp import create_app
from webapp.python_news import get_news

app = create_app()
with app.app_context():
    get_news()