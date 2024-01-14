from website import create_app
from flask import request , redirect
import logging

# Set up logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Create a logger for your application
logger = logging.getLogger('Spynet')
logger.setLevel(logging.INFO)

# Create a file handler and set the format
log_file_path = 'access_log.txt'
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - IP: %(client_ip)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ...

app = create_app()

# Paths to exclude from logging
excluded_paths = ['/logs', '/favicon.ico']

@app.before_request
def log_request_info():
    ip_address = request.headers.get('HTTP_CF_CONNECTING_IP') or request.remote_addr
    request.client_ip = ip_address

@app.after_request
def log_response_info(response):
    ip_address = getattr(request, 'client_ip', 'UNKNOWN')

    # Check if the path should be excluded from logging
    if request.path not in excluded_paths:
        logger.info(f"{request.method} {request.url} - Status: {response.status_code} - IP: {ip_address}")

    return response


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    from waitress import serve
    serve(app, host="0.0.0.0", port=80, _quiet=True)

