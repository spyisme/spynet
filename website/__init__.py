# __init__.py
from flask import Flask, request, redirect, url_for , render_template   
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO , emit
from flask_mail import Mail , Message
import os
from datetime import datetime , timezone
import pytz

mail = Mail()


db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
connected_clients = 0



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


    def read_html_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    
    @app.route('/send_email', methods=['GET', 'POST'])
    def send_email():
        if request.method == 'GET':
            recipient = request.args.get('to')
            subject = "Account Registration Confirmation"

            html_content = read_html_file('website/templates/users_pages/email.html')

            msg = Message(subject, recipients=[recipient])
            msg.html = html_content

            try:
                mail.send(msg)
                return redirect("/register?done=true")
            except Exception as e:
                return f"Failed to send email. Error: {str(e)}"

        return "This endpoint only accepts GET requests."




    @app.route('/refreshpage')
    def refresh_page():
        user = request.args.get('user')
        if current_user.username == 'spy'  :
            socketio.emit('refresh', namespace='/')
            return 'Page refresh signal sent to all clients'
        return redirect(url_for('views.home'))
    
    @app.route('/count')
    def count():
        return str(connected_clients)

    @app.route('/admin')
    def admin():
        if current_user.username != 'spy' :
            users = User.query.filter(User.username != 'biba').all()

        else :
            users = User.query.all()

        return render_template('admin/admin.html',users = users ,connected_clients=connected_clients)


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
    
    
    import json , requests

    def discord_log(message):
        messageeeee = { 'content': message }
        payload = json.dumps(messageeeee)
        headers = {'Content-Type': 'application/json'}
        requests.post("https://discord.com/api/webhooks/1220549855185997935/mkFuF-omKjobn77rSBMPqC6cYz2ddGUZGGc0VigjLs0J43cGwApQtQUlB6s1tDuCIQnt", data=payload, headers=headers)
    def discord_log2(message):
        messageeeee = { 'content': message }
        payload = json.dumps(messageeeee)
        headers = {'Content-Type': 'application/json'}
        requests.post("https://discord.com/api/webhooks/1224087481255723049/fSB0MRQEV2ihjm19SuMMsnrKxokxn-2MVS7M-iBAh1tjZq3vs3caMK_830-jQG0AAAEp", data=payload, headers=headers)
       
    # Before request callback to check if the user is logged in
    def before_request():

        excluded_routes = [
            'views.logoutotherdevices','views.login2','views.login','views.registeracc', 'views.verifyemail',
            'views.robots_txt','views.favicon', 'views.monitor',
            'shortlinks.tools', 'vdo.commandslist', 'shortlinks.youtube', 
            'vdo.cmdcommand' , 'vdo.storjflask2', 
            'views.loginnochecks'
            ]
        

        if request.endpoint and request.endpoint not in excluded_routes and not request.path.startswith('/static/') and not request.path.startswith('/send_email'):
            if not current_user.is_authenticated:
                return redirect(url_for('views.login'))
            else:
                client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
                user_agent = request.headers.get('User-Agent')

                utc_now = datetime.now(timezone.utc)

                gmt2 = pytz.timezone('Etc/GMT-2')
                gmt2_now = utc_now.replace(tzinfo=pytz.utc).astimezone(gmt2)
                timestamp = gmt2_now.strftime('%d/%m -- %I:%M %p')

                device_type = "Desktop" if "Windows" in user_agent else ("Macintosh" if "Macintosh" in user_agent else "Mobile")


                blueprint = request.endpoint.split('.')[0]

                if not request.path.startswith('/static/'):
                    if request.path.startswith('/redirect/'):
                        request.path = request.path.split('/')
                        request.path = '/'.join( request.path[2:])
                        request.path =  request.path.replace('questionmark', '?')
                        request.path =  request.path.replace('andsympol', '&')
                    else :
                        request.path = request.url
                if current_user and current_user.username not in  ['spy','biba', 'skailler'] and blueprint != "vdo" :
                        log_message = f"{client_ip} === {request.path} === {timestamp} === {device_type}\n"
                        
                        log_directory = os.path.join('logs', f"{current_user.username}_log.txt")
                        if "/logs" not in request.path: 
                            with open(log_directory, 'a') as log_file:
                                log_file.write(log_message)

                        discord_log(f"{client_ip} Viewed <{request.path}>  {current_user.username} {device_type} ```{user_agent}```")
                        discord_log2(f"{client_ip} Viewed <{request.path}>  {current_user.username} {device_type} ```{user_agent}```")

                else :
                        discord_log2(f"{client_ip} Viewed <{request.path}>  {current_user.username} {device_type} ```{user_agent}```")

                        log_message = f"{client_ip} === {request.path} === {timestamp} === {device_type}\n"
                        log_directory = os.path.join('logs', f"{current_user.username}_log.txt")
                        if "/logs" not in request.path: 
                            with open(log_directory, 'a') as log_file:
                                log_file.write(log_message)


            
    app.before_request(before_request)


    return app , socketio

connected_usernames = set()

@socketio.on('connect', namespace='/')
def handle_connect():
    global connected_clients, connected_usernames
    connected_clients += 1
    username = current_user.username  # Assuming current_user.username is available
    connected_usernames.add(username)  # Add the username to the set
    emit('update_clients', {'count': connected_clients, 'username': username}, broadcast=True)
    return

@socketio.on('disconnect', namespace='/')
def handle_disconnect():
    global connected_clients, connected_usernames
    connected_clients -= 1
    username = current_user.username  # Assuming current_user.username is available
    connected_usernames.remove(username)  # Remove the username from the set
    emit('update_clients', {'count': connected_clients, 'username': username}, broadcast=True)
    return