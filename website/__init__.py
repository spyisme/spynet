from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Set a secret key for your app (change this to a strong, random value in production)
    app.config['SECRET_KEY'] = 'secretkey'

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .shortlinks import shortlinks
    app.register_blueprint(shortlinks, url_prefix='/')

    return app
