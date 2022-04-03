from flask import Flask, render_template
from flask_login import LoginManager
from webapp.news.models import db, News
from webapp.news.weather import weather_by_city
from webapp.user.models import User
from webapp.news.views import blueprint as index_blueprint
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.admin_page import blueprint as admin_blueprint



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(index_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app