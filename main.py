from website import create_app
from flask import request, redirect
import logging
import os
import fnmatch
from flask_login import login_required

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

excluded_urls = {'http://spysnet.com/logs', 'http://wwww.spysnet.com/logs' , 'http://spysnet.com/favicon.ico','http://www.spysnet.com/favicon.ico'}
pattern = 'http://spysnet.com/static/*'
excluded_urls.add(pattern)
www_pattern = 'http://www.spysnet.com/static/*'
excluded_urls.add(www_pattern)
vdo = 'http://www.spysnet.com/vdocipher?token=*'
excluded_urls.add(vdo)



@app.before_request
def log_request_info():
    client_ip = request.headers['CF-Connecting-IP']
    with open("bannedips.txt") as file:
        lines = [line.rstrip() for line in file]
    if client_ip in lines:
        return " ", 403
    if any(fnmatch.fnmatch(request.url, pattern) or fnmatch.fnmatch(request.url, www_pattern) for pattern in excluded_urls or fnmatch.fnmatch(request.url, vdo) for pattern in excluded_urls):

        return
    if 'CF-Connecting-IP' in request.headers:
        ip_address = request.headers['CF-Connecting-IP']
    else:
        ip_address = request.remote_addr
    if "UptimeRobot" in  request.user_agent.string:
        return    
    user_agent = request.user_agent
    
    logger.info(f"IP Address: {ip_address} accessed {request.url} , {user_agent}")

@app.route('/ban_ip')
@login_required
def ban_ip():
    ip_to_ban = request.args.get('ip')

    if ip_to_ban:
        with open("bannedips.txt", "a") as myfile:
            myfile.write(f"{ip_to_ban}\n")  
        return f"IP {ip_to_ban} has been banned."
    else:
        return "No IP provided in the query parameters.", 400

@app.route("/unbanall")
@login_required
def unbanall():
    with open("bannedips.txt", 'w'):
        pass 
        return "done"


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    from waitress import serve
    serve(app, host="0.0.0.0", port=80, _quiet=True)




