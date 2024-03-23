# __init__.py
from flask import Flask, request, redirect, url_for, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import json, requests
from datetime import datetime, timedelta, timezone
from flask_login import logout_user
from flask_socketio import SocketIO, emit

socketio = SocketIO()
db = SQLAlchemy()
login_manager = LoginManager()
connected_clients = 0


def create_app():

  app = Flask(__name__)

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
  banned_ips = []

  @app.route('/refreshpage')
  def refresh_page():
    if current_user.username == 'spy':
      socketio.emit('refresh', namespace='/')
      return 'Page refresh signal sent to all clients'
    return redirect(url_for('views.home'))

  @app.route('/admin')
  def admin():
    if current_user.username in ['spy', 'skailler']:
      all_users = User.query.all()

      return render_template('admin.html',
                             users=all_users,
                             connected_clients=connected_clients,
                             banned_ips=banned_ips)
    else:
      return redirect(url_for('views.home'))

  @app.route('/banip', methods=['GET'])
  def ban_ip():
    ip = request.args.get('ip')
    if ip:
      banned_ips.append(ip)
      return jsonify({'message': f'IP {ip} added to the excluded list.'}), 200
    else:
      return jsonify(
          {'error': 'IP address not provided in the request parameters.'}), 400

  @app.route('/unbanip', methods=['GET'])
  def unban_ip():
    ip = request.args.get('ip')
    if ip:
      if ip in banned_ips:
        banned_ips.remove(ip)
        return jsonify({'message': f'IP {ip} has been unbanned.'}), 200
      else:
        return jsonify({'error': f'IP {ip} is not in the banned list.'}), 404
    else:
      return jsonify(
          {'error': 'IP address not provided in the request parameters.'}), 400

  @app.route('/unbanallips', methods=['GET'])
  def unbanall():
    banned_ips.clear()
    return jsonify(
        {'message': 'All IPs have been removed from the excluded list.'})
#Main
  def before_request():
    excluded_routes = [
        'views.random_song', 'views.monitor', 'views.new', 'views.favicon',
        'shortlinks.netflix', 'vdo.iframevids', 'views.login', 'views.login2',
        'shortlinks.tools', 'vdo.commandslist', 'shortlinks.youtube',
        'vdo.cmdcommand', 'vdo.storjflask2'
    ]
    Request_type = ""
    if request.endpoint and request.endpoint not in excluded_routes and not request.path.startswith(
        '/static/'):

      if not current_user.is_authenticated:
        return redirect(url_for('views.login'))
      else:
        if current_user.username != 'spy':
          if current_user.username == 'ss2':
            current_user.username = "ss"
          client_ip = request.headers['X-Forwarded-For'].split(',')[1].strip()
          if client_ip in banned_ips:
            return jsonify({'error': f'Banned [{client_ip}]'}), 403

          # Rate limiting
          request_count_key = f'request_count_{client_ip}'
          timestamp_key = f'timestamp_{client_ip}'
          now = datetime.now(timezone.utc)  # Making now offset-aware
          request_count = session.get(request_count_key, 0)
          last_request_time = session.get(timestamp_key)

          if last_request_time and now - last_request_time < timedelta(
              seconds=10):
            request_count += 1
            session[request_count_key] = request_count
            if request_count >= 20:
              banned_ips.append(client_ip)
              logout_user()
              discord_log(f'Banned [{client_ip}] <@709799648143081483>')

              return jsonify({'error': f'Banned [{client_ip}]'}), 403
          else:
            session[request_count_key] = 1

          session[timestamp_key] = now

          user_agent = request.headers.get('User-Agent')
          if not request.path.startswith('/static/'):

            if request.path.startswith('/redirect/'):
              request.path = request.path.split('/')
              request.path = '/'.join(request.path[2:])
              request.path = request.path.replace('questionmark', '?')
              request.path = request.path.replace('andsympol', '&')
            else:
              request.path = f"https://spysnet.com{request.path}"
            if request.method != "GET":
              Request_type = request.method

            discord_log(
                f"{client_ip} - {current_user.username} Viewed <{request.path}> {Request_type} Device ```{user_agent}```"
            )

  app.before_request(before_request)

  return app, socketio


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
