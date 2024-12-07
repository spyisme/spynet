# __init__.py
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
import json, requests  

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()



def create_app():

    app = Flask(__name__)

    # Configuration for Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'amooraymanh730072@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ocpb mxsf ncwu pebf'
    app.config['MAIL_DEFAULT_SENDER'] = 'sanawyasessions@spysnet.com'

    mail.init_app(app)


    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = b'ssss'  


    db.init_app(app)
    login_manager.init_app(app)
    
    from .website import website
    app.register_blueprint(website, url_prefix='/')

    from .shortlinks import shortlinks
    app.register_blueprint(shortlinks, url_prefix='/')

    from .vdo import vdo
    app.register_blueprint(vdo, url_prefix='/')

    from .ecu import ecu
    app.register_blueprint(ecu, url_prefix='/')

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def discord_log(message):
        messageeeee = {'content': message}
        payload = json.dumps(messageeeee)
        headers = {'Content-Type': 'application/json'}
        requests.post("https://discord.com/api/webhooks/1220549855185997935/mkFuF-omKjobn77rSBMPqC6cYz2ddGUZGGc0VigjLs0J43cGwApQtQUlB6s1tDuCIQnt",data=payload,headers=headers)
        


    # Before request callback to check if the user is logged in
    def before_request():

        excluded_routes = [
            'website.logoutotherdevices', 'website.login2', 'website.login', 'website.secure_endpoint', "ecu.ecumid1ch", "ecu.nexichatapi",
            'website.registeracc', 'website.forgotpassword', 'website.robots_txt',"ecu.computerpdfs",
            'website.favicon', 'website.monitor', 'shortlinks.tools',"vdo.skillshare","shortlinks.shorturl",
            'vdo.commandslist', 'shortlinks.youtube', 'vdo.cmdcommand', "ecu.english_assignment",
            'vdo.storjflask2' , 'website.uptimebackup' , 'website.home' , 'shortlinks.netflix' , 'website.check_username']
        

        if request.host.startswith("www."):
            non_www_host = request.host[4:]  # Remove 'www.'
            url = request.url.replace(request.host, non_www_host)
            return redirect(url, code=301)
        

        if request.endpoint and request.endpoint not in excluded_routes and not request.path.startswith(
                '/static/') :
            if not current_user.is_authenticated:
                return redirect(url_for('website.home'))

            

            elif current_user.otp == "Waiting approval" :
                if not request.path.startswith('/logout') :
                    return render_template('users_pages/approve.html')
                

            elif current_user.password == "Chnageme":
                if not request.path.startswith('/change_password') :
                    return  redirect(url_for('website.change_password'))          

            else:
                client_ip = request.headers.get('X-Forwarded-For')
                if client_ip:
                    client_ip = client_ip.split(',')[0].strip()
                else:
                    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)

                user_agent = request.headers.get('User-Agent')


                device_type = "Desktop" if "Windows" in user_agent else (
                    "Macintosh" if "Macintosh" in user_agent else "Mobile")


                if "logs" not in request.path :
                    if len(request.path) > 1 :
                        if request.method == 'GET' :
                            if request.path.startswith('/redirect/'):
                                request.path = request.path.split('/')
                                request.path = '/'.join(request.path[2:])
                                request.path = request.path.replace('questionmark', '?')
                                request.path = request.path.replace('andsympol', '&')
  

                if not request.path.startswith('/static/'):
                        if any(keyword in request.path for keyword in ["drive", "youtube"]):
                            pass
                        else:
                            request.path = request.url

            

                if current_user and current_user.username not in ['spy']:
                    
                    discord_log(f"{client_ip} Viewed <{request.path}>  {current_user.username} {device_type} ```{user_agent}```")

    app.before_request(before_request)

    return app
