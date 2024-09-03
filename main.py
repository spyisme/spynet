import logging  #type: ignore
import json
import requests
from flask import render_template, request, redirect , url_for , jsonify
from website import create_app
import hmac
import hashlib
from flask_login import current_user

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app, socketio = create_app()




@app.errorhandler(404)
def page_not_found(e):  #type: ignore
    if request.path.endswith('/'):
        return redirect(request.path[:-1])
    if "admin" in request.path or "edit" in request.path:
        if current_user.type == "admin" :
            return redirect(url_for('views.admin'))

    return render_template('used_pages/404.html')



SECRET_KEY = b'ss'  # Should be securely generated and consistent

def generate_signature(message, secret_key):
    return hmac.new(secret_key, message.encode(), hashlib.sha256).hexdigest()

@app.route('/secure-endpoint', methods=['POST'])
def secure_endpoint():
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({"status": "missing message"}), 400

    response_data = {"status": "false", "message": message}
    # Serialize the data consistently
    data_string = json.dumps(response_data, sort_keys=True)
    response_signature = generate_signature(data_string, SECRET_KEY)

    return jsonify({"data": response_data, "signature": response_signature}), 200



if __name__ == "__main__":
    socketio.run(app,
                 host="0.0.0.0",
                 port=80,
                 allow_unsafe_werkzeug=True,
                 debug=True,
                 use_reloader=True,
                 log_output=True)
