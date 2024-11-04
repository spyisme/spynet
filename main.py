import logging  #type: ignore
import json
import requests
from flask import render_template, request, redirect , url_for , jsonify
from website import create_app
from flask_login import current_user

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app, socketio = create_app()


@app.errorhandler(404)
def page_not_found(e):  

    if request.path.endswith('/'):
        return redirect(request.path[:-1])
    
    if current_user.is_authenticated :
        if current_user.type :
            if "admin" in request.path or "edit" in request.path:
                if current_user.type == "admin" :
                    return redirect(url_for('views.admin'))

    return render_template('used_pages/404.html' , error = e)



if __name__ == "__main__":
    socketio.run(app,
                 host="0.0.0.0",
                 port=80,
                 allow_unsafe_werkzeug=True,
                 debug=True,
                 use_reloader=True,
                 log_output=True)
