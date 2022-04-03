from flask import Blueprint, current_app, render_template, current_app
from webapp.news.models import db, News
from webapp.news.weather import weather_by_city

blueprint = Blueprint('index', __name__, url_prefix='/')

@blueprint.route('/')
def index():
    title = 'Webpage'
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template('index.html', page_title=title, weather=weather, news_list=news_list)