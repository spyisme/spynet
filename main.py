import logging  #type: ignore
import json
import requests
from flask import render_template, request
from website import create_app

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app, socketio = create_app()


@app.errorhandler(404)
def page_not_found(e):  #type: ignore
    if "update" in request.path:
        split_string = request.path.split("update")
        requested_url = split_string[0] + "/update" + split_string[1]

        return render_template('used_pages/404.html',
                               update=True,
                               requested_url=requested_url)
    return render_template('used_pages/404.html')


def discord_log_backend(text):
    message = {'content': text}
    payload = json.dumps(message)
    headers = {'Content-Type': 'application/json'}
    requests.post(
        "https://discord.com/api/webhooks/1264918948730638336/nD1A8OVB0FmSgUVV7DCd2gumd7CBeTWAoq7AbqjCjwoRRkkgLRM7a8xuYRPOUos4AmwE",
        data=payload,
        headers=headers)


if __name__ == "__main__":
    socketio.run(app,
                 host="0.0.0.0",
                 port=80,
                 allow_unsafe_werkzeug=True,
                 debug=True,
                 use_reloader=True,
                 log_output=True)
