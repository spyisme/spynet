# __init__.py
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Replace 'sqlite:///site.db' with your actual database URL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'secretkey'

    db.init_app(app)
    login_manager.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .shortlinks import shortlinks
    app.register_blueprint(shortlinks, url_prefix='/')

    from .vdo import vdo
    app.register_blueprint(vdo, url_prefix='/')

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Before request callback to check if the user is logged in
    def before_request():
        # List of routes that don't require login
        excluded_routes = ['views.login', 'views.home']

        # Exclude all routes from the 'shortlinks' blueprint
        if request.endpoint and request.endpoint.startswith('shortlinks.'):
            excluded_routes.append(request.endpoint)

        if request.endpoint and request.endpoint not in excluded_routes:
            if not current_user.is_authenticated:
                # Redirect to the login page if the user is not logged in
                return "Login Please"

    #app.before_request(before_request)

    return app
