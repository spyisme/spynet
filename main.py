from website import create_app
from flask import  redirect 
import logging


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/all')



@app.errorhandler(500)
def internal_error(error):
    error_message = f"500 error: {str(error)}"
    return error_message, 500

if __name__ == "__main__":
    app.debug = True  
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
