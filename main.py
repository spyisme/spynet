from website import create_app
from flask import request, redirect , jsonify
import logging

import os 



os.system('title Spynet')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logger = logging.getLogger('Spynet')
logger.setLevel(logging.INFO)


app = create_app()



@app.before_request
def ipwhitelis():
    with open("allowedips.txt") as file:
        lines = [line.rstrip() for line in file]

    if 'CF-Connecting-IP' in request.headers:
        ip_address = request.headers['CF-Connecting-IP']
    else:
        ip_address = request.remote_addr
        with open("allowedips.txt", "a") as file:
            file.write(f"{ip_address}\n")


    if ip_address not in lines:
        return jsonify({'Ip': f'{ip_address}'})
    
        #return render_template('test.html', ip_address=ip_address), 403    



@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    from waitress import serve
    serve(app, host="0.0.0.0", port=80, _quiet=True)




