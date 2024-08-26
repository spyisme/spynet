# __init__.py
from flask import Flask, request, redirect, url_for, render_template , send_file #type: ignore
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, emit
from flask_mail import Mail, Message
from datetime import datetime, timezone
import pytz
import random
import json, requests  #type: ignore
import os 
from flask_cors import CORS
from datetime import datetime, timedelta

mail = Mail()

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

connected_clients = 0


def create_app():

    app = Flask(__name__)
    CORS(app, resources={r"/iframes": {"origins": "https://omar-sherbeni.com"}})

    # Configuration for Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'amooraymanh730072@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ocpb mxsf ncwu pebf'
    app.config['MAIL_DEFAULT_SENDER'] = 'sanawyasessions@spysnet.com'

    mail.init_app(app)

    def read_html_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()



    
    @app.route('/refreshpage')
    def refresh_page():
        if current_user.username == 'spy':
            socketio.emit('refresh', namespace='/')
            return 'Page refresh signal sent to all clients'
        return redirect(url_for('views.home'))






    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'secretkey'


    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
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

    def discord_log(message):
        messageeeee = {'content': message}
        payload = json.dumps(messageeeee)
        headers = {'Content-Type': 'application/json'}
        requests.post(
            "https://discord.com/api/webhooks/1220549855185997935/mkFuF-omKjobn77rSBMPqC6cYz2ddGUZGGc0VigjLs0J43cGwApQtQUlB6s1tDuCIQnt",
            data=payload,
            headers=headers)
        


    # Before request callback to check if the user is logged in




    def before_request():

        excluded_routes = [
            'views.logoutotherdevices', 'views.login2', 'views.login',
            'views.registeracc', 'views.forgotpassword', 'views.robots_txt',
            'views.favicon', 'views.monitor', 'shortlinks.tools',
            'vdo.commandslist', 'shortlinks.youtube', 'vdo.cmdcommand',
            'vdo.storjflask2' , 'views.uptimebackup' , 'views.home' , 'shortlinks.netflix' , 'views.check_username'
        ]

        if request.endpoint and request.endpoint not in excluded_routes and not request.path.startswith(
                '/static/') :
            if not current_user.is_authenticated:
                token = request.args.get('token')
                if request.path.startswith("/iframes"):
                    if token!= "spyisme" :
                        return redirect(url_for('views.home'))
                else :
                    return redirect(url_for('views.home'))

            

            elif current_user.otp == "Waiting approval" :

                if not request.path.startswith('/send_email') :

                    return render_template('users_pages/approve.html')
                

            elif current_user.password == "Chnageme":
                if not request.path.startswith('/change_password') :
                    return  redirect(url_for('views.change_password'))  
                


            elif current_user.subscription_date + timedelta(days=30) < datetime.today().date() :
                if current_user.type != 'admin' :
                    return render_template('users_pages/expired.html')
        

            else:
                client_ip = request.headers.get('X-Forwarded-For')
                if client_ip:
                    client_ip = client_ip.split(',')[0].strip()
                else:
                    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)

                user_agent = request.headers.get('User-Agent')

                utc_now = datetime.now(timezone.utc)

                gmt2 = pytz.timezone('Etc/GMT-3')
                gmt2_now = utc_now.replace(tzinfo=pytz.utc).astimezone(gmt2)
                timestamp = gmt2_now.strftime('%d/%m -- %I:%M:%S %p')


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
                            log_value = f"{client_ip} | {device_type} | {request.path} | {timestamp}"   
                            logs_list = json.loads(current_user.logs) if current_user.logs else []
                            logs_list.append(log_value)
                            current_user.logs = json.dumps(logs_list)
                            db.session.commit()



                if not request.path.startswith('/static/'):
                        if any(keyword in request.path for keyword in ["drive", "youtube"]):

                            pass
                        else:

                            request.path = request.url

            

                if current_user and current_user.username not in ['spy']:
                    discord_log(f"{client_ip} Viewed <{request.path}>  {current_user.username} {device_type} ```{user_agent}```")

    app.before_request(before_request)

    return app, socketio


user_socket_map = {}


@socketio.on('connect', namespace='/')
def handle_connect():
    global connected_clients
    connected_clients += 1
    emit('update_clients', {'count': connected_clients}, broadcast=True)


@socketio.on('register', namespace='/')
def handle_register(data):
    user_id = data.get('user')
    if user_id:
        user_socket_map[user_id] = request.sid


@socketio.on('disconnect', namespace='/')
def handle_disconnect():
    global connected_clients
    connected_clients -= 1

    # Remove the user from the mapping
    user_id = None
    for usr_id, sid in user_socket_map.items():
        if sid == request.sid:
            user_id = usr_id
            break
    if user_id:
        del user_socket_map[user_id]

    emit('update_clients', {'count': connected_clients}, broadcast=True)
