from website import create_app

from flask import render_template
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app , socketio = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('used_pages/404.html')

@app.errorhandler(Exception)
def exception_handler(error):
    return render_template('used_pages/500.html' , error = error)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=80, allow_unsafe_werkzeug=True , debug=True)



# @app.errorhandler(404)
# def page_not_found(e):


#     print(request.headers)

#     print(request.url)
#     return f"404 Error - User tried to access: {request.url}"
