from website import create_app
from flask import redirect, render_template
import sys
from io import StringIO

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/all')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
