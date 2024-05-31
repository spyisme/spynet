from website import create_app
import requests , json
from flask import render_template , request
import logging
from flask_login import  current_user 

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app , socketio = create_app()


@app.errorhandler(404)
def page_not_found(e):
    if "update" in request.path :
        split_string = request.path.split("update")
        requested_url = split_string[0] + "/update" + split_string[1]

        return render_template('used_pages/404.html' , update = True , requested_url = requested_url)
    return render_template('used_pages/404.html')




def discord_log_backend(text):
    message = { 'content': text }
    payload = json.dumps(message)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1223859771401179146/Qaxf4CVfRhTn7oQ2lbz1MdJQZ441_-VruTkP8tir3JabeFbMkLR9aJpDANDwFSYcEDfJ", data=payload, headers=headers)


@app.errorhandler(Exception)
def exception_handler(error):
    if current_user.username != 'spy' : 
        discord_log_backend(f'User : {current_user.username} encountered an error while trying to access {request.url} ```{error}``` <@709799648143081483>')
        return render_template('used_pages/500.html' , error = error)




if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=80, allow_unsafe_werkzeug=True , debug=True)



# @app.errorhandler(404)
# def page_not_found(e):


#     print(request.headers)

#     print(request.url)
#     return f"404 Error - User tried to access: {request.url}"
