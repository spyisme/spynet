from website import create_app
from flask import  redirect 
import logging


from os import system
system("title Spynet")

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/all')



if __name__ == "__main__":
    app.debug = True  
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)