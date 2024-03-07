# __init__.py
from flask import Flask, request, redirect, url_for , render_template   
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO , emit


db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
connected_clients = 0




def create_app():

    app = Flask(__name__)


    
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
        if current_user.username in ['spy', 'skailler']:
        
            all_users = User.query.all()
            return render_template('admin.html', users=all_users , connected_clients = connected_clients)
        
        else :
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
    
    import json , requests

    def discord_log(message):
        messageeeee = { 'content': message }
        payload = json.dumps(messageeeee)
        headers = {'Content-Type': 'application/json'}
        requests.post("https://discord.com/api/webhooks/1212485016903491635/4BZmlRW3o2LHBD2Rji5wZSRAu-LonJZIy-l_SvMaluuCSB_cS1kuoofhtPt2pq2m6AuS", data=payload, headers=headers)

    # Before request callback to check if the user is logged in
    def before_request():
        excluded_routes = ['views.random_song','views.monitor','views.new','views.favicon' ,'shortlinks.netflix' ,'vdo.iframevids','views.login', 'shortlinks.tools', 'vdo.commandslist', 'shortlinks.youtube', 'vdo.cmdcommand' , 'vdo.storjflask2']
        Request_type =""
        if request.endpoint and request.endpoint not in excluded_routes and not request.path.startswith('/static/'):
            if not current_user.is_authenticated:
                return redirect(url_for('views.login'))
            else:
                if current_user.username != 'spy' :
                    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
                    user_agent = request.headers.get('User-Agent')
                    if not request.path.startswith('/static/'):

                        if request.path.startswith('/redirect/'):

                            request.path = request.path.split('/')
                            request.path = '/'.join( request.path[2:])
                            request.path =  request.path.replace('questionmark', '?')
                            request.path =  request.path.replace('andsympol', '&')
                        else :
                            request.path = f"https://spysnet.com{request.path}"
                        if request.method != "GET":
                            Request_type = request.method
                            
                        discord_log(f"{client_ip} Viewed <{request.path}> {Request_type} {current_user.username} Device ```{user_agent}```")


    app.before_request(before_request)


    return app , socketio

@socketio.on('connect', namespace='/')
def handle_connect():
    global connected_clients
    connected_clients += 1
    emit('update_clients', {'count': connected_clients}, broadcast=True)
    return

@socketio.on('disconnect', namespace='/')
def handle_disconnect():
    global connected_clients
    connected_clients -= 1
    emit('update_clients', {'count': connected_clients}, broadcast=True)
    return

