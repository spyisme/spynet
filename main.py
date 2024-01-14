from website import create_app
from flask import request, redirect
import logging
import os
import fnmatch

# Set up logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Create a logger for your application
logger = logging.getLogger('Spynet')
logger.setLevel(logging.INFO)

# Create a file handler and set the format
log_file_path = 'access_log.txt'
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ...

app = create_app()

excluded_urls = {'http://spysnet.com/favicon.ico', 'http://spysnet.com/logs'}
pattern = 'http://spysnet.com/static/assets/*'
excluded_urls.add(pattern)

@app.before_request
def log_request_info():
    if any(fnmatch.fnmatch(request.url, pattern) for pattern in excluded_urls):
        return
    if 'CF-Connecting-IP' in request.headers:
        ip_address = request.headers['CF-Connecting-IP']
    else:
        ip_address = request.remote_addr
    user_agent = request.user_agent
    device_details = f"Device: {user_agent.platform} - Browser: {user_agent.browser} - Version: {user_agent.version}"

    logger.info(f"IP Address: {ip_address} accessed {request.url} , {user_agent}")

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    from waitress import serve
    serve(app, host="0.0.0.0", port=80, _quiet=True)




