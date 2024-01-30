from website import create_app
from flask import request , redirect , render_template
import logging
import os
import sys
import time
import threading
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = create_app()



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
